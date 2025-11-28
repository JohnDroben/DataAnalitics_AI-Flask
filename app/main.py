from flask import Flask, request, jsonify
from flask_cors import CORS
from .services.analysis_service import AnalysisService
from .utils.file_handler import validate_file
from .utils.logger import logger
from flask import render_template
import os
import logging
import pandas as pd
import numpy as np

# Используем наш кастомный логгер
app = Flask(__name__)
CORS(app)
analysis_service = AnalysisService()

# In-memory data store
data_store = {
    "dataframe": None,
    "text_data": None,
    "filename": None,
    "data_type": None  # 'table' or 'text'
}

@app.route('/')
def home():
    logger.info("Home page requested")
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    logger.info("=" * 80)
    logger.info("📁 UPLOAD REQUEST RECEIVED")
    logger.info(f"Content-Type: {request.content_type}")
    logger.info(f"Files: {list(request.files.keys())}")
    
    if 'file' not in request.files:
        logger.error("❌ No file found in request")
        return jsonify({"status": "error", "message": "Файл не найден"}), 400

    file = request.files['file']
    logger.info(f"📄 File received: {file.filename}")
    logger.info(f"   Size: {file.content_length} bytes")
    
    try:
        logger.info("🔍 Validating file...")
        validate_file(file)
        logger.info("✅ File validation passed")
        
        logger.info("💾 Saving file to uploads folder...")
        file_path = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(file_path)
        logger.info(f"✅ File saved to: {file_path}")
        logger.info(f"   File exists: {os.path.exists(file_path)}")
        logger.info(f"   File size: {os.path.getsize(file_path)} bytes")

        logger.info("🤖 Starting file analysis...")
        analysis_result = analysis_service.analyze_file(file_path)
        logger.info("✅ File analysis completed")
        
        if isinstance(analysis_result.get("data"), pd.DataFrame):
            data_store["dataframe"] = analysis_result["data"]
            data_store["text_data"] = None
            data_store["data_type"] = "table"
            data_store["filename"] = file.filename
            df = data_store["dataframe"]
            logger.info(f"✅ Data stored successfully")
            logger.info(f"   Rows: {len(df)}")
            logger.info(f"   Columns: {list(df.columns)}")
            return jsonify({
                "status": "success",
                "filename": file.filename,
                "rows": len(df),
                "columns": list(df.columns)
            })
        else:
            # Handle non-dataframe data (e.g., from PDF)
            data_store["dataframe"] = None
            data_store["text_data"] = analysis_result.get("data")
            data_store["data_type"] = "text"
            data_store["filename"] = file.filename
            
            text_data = data_store["text_data"]
            text_length = len(text_data) if isinstance(text_data, str) else 0
            
            logger.info("⚠️ File processed but data is not a DataFrame")
            logger.info(f"   Data type: {type(analysis_result.get('data'))}")
            logger.info(f"   Text length: {text_length} characters")
            
            return jsonify({
                "status": "success",
                "filename": file.filename,
                "message": "File processed successfully",
                "data_type": "text",
                "content_length": text_length
            })

    except Exception as e:
        logger.error(f"❌ Error during file upload: {type(e).__name__}: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

@app.route('/api/data', methods=['GET'])
def get_data():
    logger.debug("Data request received")
    data_type = data_store.get("data_type")
    
    if data_type == "table":
        df = data_store.get("dataframe")
        if df is None:
            logger.warning("No table data available in data store")
            return jsonify({"error": "No data available"}), 404

        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 100))
        logger.debug(f"Returning table data slice: offset={offset}, limit={limit}")
        
        df_slice = df.iloc[offset:offset+limit]

        # Replace NaN with None and convert numpy types to Python native types
        def sanitize_row(row):
            sanitized = {}
            for k, v in row.items():
                if pd.isna(v):
                    sanitized[k] = None
                elif isinstance(v, (np.integer,)):
                    sanitized[k] = int(v)
                elif isinstance(v, (np.floating,)):
                    sanitized[k] = float(v)
                elif isinstance(v, (np.bool_,)):
                    sanitized[k] = bool(v)
                elif hasattr(v, 'item') and isinstance(v, np.generic):
                    try:
                        sanitized[k] = v.item()
                    except Exception:
                        sanitized[k] = str(v)
                else:
                    sanitized[k] = v
            return sanitized

        rows = [sanitize_row(r) for r in df_slice.to_dict(orient='records')]

        return jsonify({
            "data_type": "table",
            "columns": list(df.columns),
            "rows": rows,
            "total_rows": len(df)
        })
    
    elif data_type == "text":
        text_data = data_store.get("text_data")
        if text_data is None:
            logger.warning("No text data available in data store")
            return jsonify({"error": "No data available"}), 404
        
        logger.debug(f"Returning text data (length: {len(text_data)} chars)")
        
        # Split text into lines for display as table rows
        lines = text_data.split('\n')
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 100))
        
        # Take a slice of lines
        sliced_lines = lines[offset:offset+limit]
        
        # Convert lines to table format (each line is a row with a single column "Content")
        rows = [{"Content": line[:1000]} for line in sliced_lines if line.strip()]  # Limit line length to 1000 chars
        
        logger.debug(f"Converted {len(rows)} text lines to table rows")
        
        return jsonify({
            "data_type": "text",
            "columns": ["Content"],
            "rows": rows,
            "total_rows": len(lines)
        })
    
    else:
        logger.warning("No data available in data store")
        return jsonify({"error": "No data available"}), 404

@app.route('/api/analysis', methods=['GET'])
def get_analysis():
    logger.info("Analysis request received")
    data_type = data_store.get("data_type")
    
    if data_type == "table":
        df = data_store.get("dataframe")
        if df is None:
            logger.warning("No table data available for analysis")
            return jsonify({"error": "No data available"}), 404

        numeric_cols = df.select_dtypes(include=['number']).columns
        # Compute sums and sanitize values to be JSON-serializable
        raw_sums = df[numeric_cols].sum()
        column_sums = {}
        for col in numeric_cols:
            v = raw_sums[col]
            if pd.isna(v):
                column_sums[col] = None
            else:
                try:
                    fv = float(v)
                    if fv.is_integer():
                        column_sums[col] = int(fv)
                    else:
                        column_sums[col] = fv
                except Exception:
                    try:
                        column_sums[col] = int(v)
                    except Exception:
                        column_sums[col] = str(v)

        unique_counts = {col: int(df[col].nunique()) for col in df.columns}

        logger.info(f"Analysis complete: {len(numeric_cols)} numeric columns")

        return jsonify({
            "data_type": "table",
            "column_sums": column_sums,
            "unique_counts": unique_counts
        })
    
    elif data_type == "text":
        text_data = data_store.get("text_data")
        if text_data is None:
            logger.warning("No text data available for analysis")
            return jsonify({"error": "No data available"}), 404
        
        # Basic text analysis
        word_count = len(text_data.split())
        char_count = len(text_data)
        line_count = len(text_data.split('\n'))
        
        logger.info(f"Text analysis complete: {char_count} chars, {word_count} words")
        
        return jsonify({
            "data_type": "text",
            "column_sums": {
                "Всего символов": char_count,
                "Всего слов": word_count,
                "Всего строк": line_count
            },
            "unique_counts": {
                "Content": 1
            }
        })
    
    else:
        logger.warning("No data available for analysis")
        return jsonify({"error": "No data available"}), 404

@app.route('/api/table-analysis', methods=['POST'])
def table_analysis():
    """
    Анализирует первые 15 строк загруженной таблицы через нейросети (GigaChat и Proxy API).
    
    Ожидаемый JSON-запрос:
    {
        "rows_count": 15  (опционально, по умолчанию 15)
    }
    
    Возвращает:
    {
        "status": "success",
        "giga_result": "результат от GigaChat",
        "proxy_result": "результат от Proxy API",
        "errors": {}
    }
    """
    logger.info("=" * 80)
    logger.info("📊 TABLE ANALYSIS REQUEST RECEIVED")
    
    # Проверяем наличие данных
    data_type = data_store.get("data_type")
    if not data_type:
        logger.error("❌ No data available in data store")
        return jsonify({
            "status": "error",
            "message": "No data loaded. Please upload a file first."
        }), 404
    
    # Получаем параметры запроса
    request_data = request.get_json() or {}
    rows_count = int(request_data.get('rows_count', 15))
    logger.info(f"  Rows count to analyze: {rows_count}")
    
    try:
        # Получаем данные в зависимости от типа
        if data_type == "table":
            df = data_store.get("dataframe")
            if df is None:
                logger.error("❌ DataFrame is None")
                return jsonify({
                    "status": "error",
                    "message": "Table data not available"
                }), 404
            
            logger.info(f"  DataFrame size: {len(df)} rows, {len(df.columns)} columns")
            data_to_analyze = df
            
        elif data_type == "text":
            text_data = data_store.get("text_data")
            if text_data is None:
                logger.error("❌ Text data is None")
                return jsonify({
                    "status": "error",
                    "message": "Text data not available"
                }), 404
            
            # Преобразуем текст в список строк
            lines = text_data.split('\n')
            data_to_analyze = [{"line": i+1, "content": line} for i, line in enumerate(lines) if line.strip()]
            logger.info(f"  Text data converted to {len(data_to_analyze)} rows")
        else:
            logger.error(f"❌ Unknown data type: {data_type}")
            return jsonify({
                "status": "error",
                "message": f"Unknown data type: {data_type}"
            }), 400
        
        # Отправляем на анализ
        logger.info(f"  🤖 Sending data to analysis service...")
        analysis_results = analysis_service.analyze_table_first_rows(data_to_analyze, rows_count=rows_count)
        
        logger.info("  ✅ Analysis completed successfully")
        logger.debug(f"  GigaChat result: {bool(analysis_results.get('giga_result'))}")
        logger.debug(f"  Proxy result: {bool(analysis_results.get('proxy_result'))}")
        logger.debug(f"  Errors: {analysis_results.get('errors')}")
        
        return jsonify({
            "status": "success",
            "giga_result": analysis_results.get("giga_result"),
            "proxy_result": analysis_results.get("proxy_result"),
            "errors": analysis_results.get("errors", {})
        })
        
    except Exception as e:
        logger.error(f"❌ Table analysis error: {type(e).__name__}: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": f"Analysis failed: {str(e)}"
        }), 500

@app.route('/api/ai_analyze', methods=['POST'])
def ai_analyze():
    df = data_store.get("dataframe")
    if df is None:
        return jsonify({"error": "No data available"}), 404
        
    data_sample = request.get_json()
    if not data_sample:
        return jsonify({"error": "No data provided for analysis"}), 400

    try:
        # Convert sample to string for the AI
        sample_str = pd.DataFrame(data_sample).to_string()
        
        # For now, let's just use the GigaChat API as an example
        giga_result = analysis_service.giga_api.send_analysis_request(sample_str)
        
        return jsonify({"answer": giga_result})
    except Exception as e:
        logging.error(f"AI analysis failed: {e}")
        return jsonify({"detail": "AI analysis failed"}), 500


@app.route('/api/chart_types', methods=['GET'])
def get_chart_types():
    # Hardcoded for now, can be dynamic based on data
    return jsonify({"chart_types": ["bar", "line"]})

@app.route('/api/charts', methods=['GET'])
def get_charts():
    df = data_store.get("dataframe")
    chart_type = request.args.get('chart_type')

    if df is None:
        return jsonify({"error": "No data available"}), 404
    if not chart_type:
        return jsonify({"error": "chart_type parameter is required"}), 400

    charts = []
    numeric_cols = df.select_dtypes(include=['number']).columns
    
    if chart_type == 'bar':
        for col in numeric_cols:
            charts.append({
                "type": "bar",
                "title": f"Bar Chart for {col}",
                "labels": df.index.astype(str).tolist(),
                "datasets": [{
                    "label": col,
                    "data": [None if pd.isna(x) else (int(x) if isinstance(x, (np.integer,)) or (isinstance(x, (int,)) and float(x).is_integer()) else float(x) if isinstance(x, (np.floating,)) or isinstance(x, (float,)) else x) for x in df[col].tolist()]
                }]
            })
    elif chart_type == 'line':
        for col in numeric_cols:
            charts.append({
                "type": "line",
                "title": f"Line Chart for {col}",
                "labels": df.index.astype(str).tolist(),
                "datasets": [{
                    "label": col,
                    "data": [None if pd.isna(x) else (int(x) if isinstance(x, (np.integer,)) or (isinstance(x, (int,)) and float(x).is_integer()) else float(x) if isinstance(x, (np.floating,)) or isinstance(x, (float,)) else x) for x in df[col].tolist()]
                }]
            })

    return jsonify(charts)

if __name__ == '__main__':
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(host='0.0.0.0', port=3000)
