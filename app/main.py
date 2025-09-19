from flask import Flask, request, jsonify
from flask_cors import CORS
from services.analysis_service import AnalysisService
from utils.file_handler import validate_file
from flask import render_template
import os
import logging

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
CORS(app)
analysis_service = AnalysisService()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Файл не найден"}), 400

    file = request.files['file']

    try:
        validate_file(file)
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        result = analysis_service.analyze_file(file_path)
        return jsonify({
            "status": "success",
            "results": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


if __name__ == '__main__':
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(host='0.0.0.0', port=5000)