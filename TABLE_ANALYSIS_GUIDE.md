# 📊 Модуль анализа таблиц через нейросети

## Описание

Новый модуль позволяет отправлять первые N строк загруженной таблицы в нейросетевые API (GigaChat и Proxy API) для получения аналитического анализа данных. Модуль автоматически формирует профессиональный системный промпт и обрабатывает ошибки.

## Архитектура

### Основные компоненты

```
┌─────────────────────────────────────────┐
│         Frontend (HTML/JS)              │
│  (POST /api/table-analysis)             │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│    Flask Backend (main.py)              │
│  Route: /api/table-analysis (POST)      │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   AnalysisService                       │
│   analyze_table_first_rows(data, rows)  │
└────────────┬────────────────────────────┘
             │
    ┌────────┴─────────┐
    │                  │
    ▼                  ▼
┌──────────────┐  ┌────────────┐
│ GigaChatAPI  │  │ ProxyAPI   │
└──────────────┘  └────────────┘
```

## API Endpoint

### POST `/api/table-analysis`

Отправляет первые N строк таблицы на анализ в нейросети.

**Запрос:**
```json
{
  "rows_count": 15
}
```

**Параметры:**
- `rows_count` (integer, optional): количество первых строк для анализа (по умолчанию: 15)

**Ответ (успех):**
```json
{
  "status": "success",
  "giga_result": "Анализ от GigaChat: Видны четкие тренды...",
  "proxy_result": "Анализ от Proxy API: Наблюдается корреляция...",
  "errors": {}
}
```

**Ответ (ошибка - нет данных):**
```json
{
  "status": "error",
  "message": "No data loaded. Please upload a file first.",
  "errors": {}
}
```

**Ответ (частичная ошибка - один из API недоступен):**
```json
{
  "status": "success",
  "giga_result": "Анализ от GigaChat...",
  "proxy_result": null,
  "errors": {
    "proxy_api": "Request timeout"
  }
}
```

## Использование (Backend - Python)

### Метод `analyze_table_first_rows()`

```python
from app.services.analysis_service import AnalysisService
import pandas as pd

# Инициализируем сервис
analysis_service = AnalysisService()

# Вариант 1: DataFrame
df = pd.read_csv('data.csv')
results = analysis_service.analyze_table_first_rows(df, rows_count=15)

# Вариант 2: Список словарей
data = [
    {'ID': 1, 'Name': 'Product_1', 'Price': 100},
    {'ID': 2, 'Name': 'Product_2', 'Price': 150},
    # ... еще 13 строк
]
results = analysis_service.analyze_table_first_rows(data, rows_count=15)

# Обработка результатов
if results['giga_result']:
    print("GigaChat анализ:", results['giga_result'])
else:
    print("GigaChat ошибка:", results['errors'].get('giga_chat'))

if results['proxy_result']:
    print("Proxy API анализ:", results['proxy_result'])
else:
    print("Proxy API ошибка:", results['errors'].get('proxy_api'))
```

### Функция сервиса в main.py

```python
@app.route('/api/table-analysis', methods=['POST'])
def table_analysis():
    """Анализирует первые N строк таблицы через нейросети."""
    
    # Получаем данные
    request_data = request.get_json() or {}
    rows_count = int(request_data.get('rows_count', 15))
    
    # Отправляем на анализ
    results = analysis_service.analyze_table_first_rows(
        data_to_analyze, 
        rows_count=rows_count
    )
    
    return jsonify({
        "status": "success",
        "giga_result": results["giga_result"],
        "proxy_result": results["proxy_result"],
        "errors": results.get("errors", {})
    })
```

## Использование (Frontend - JavaScript)

### Пример 1: Анализ с параметрами по умолчанию

```javascript
// Отправляем запрос с параметрами по умолчанию (15 строк)
async function analyzeTableDefault() {
  try {
    const response = await fetch('/api/table-analysis', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({})
    });
    
    const data = await response.json();
    
    if (data.status === 'success') {
      displayAnalysis(data.giga_result, data.proxy_result);
    } else {
      showError(data.message);
    }
  } catch (error) {
    console.error('Ошибка при анализе:', error);
  }
}
```

### Пример 2: Анализ с пользовательским количеством строк

```javascript
// Анализируем только первые 10 строк
async function analyzeTableCustom() {
  const rowsCount = 10;
  
  try {
    const response = await fetch('/api/table-analysis', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        rows_count: rowsCount
      })
    });
    
    const data = await response.json();
    
    if (data.status === 'success') {
      // Отображаем результаты
      if (data.giga_result) {
        document.getElementById('giga-analysis').textContent = data.giga_result;
      }
      
      if (data.proxy_result) {
        document.getElementById('proxy-analysis').textContent = data.proxy_result;
      }
      
      // Показываем ошибки если они есть
      if (Object.keys(data.errors).length > 0) {
        console.warn('Некоторые API недоступны:', data.errors);
      }
    }
  } catch (error) {
    console.error('Ошибка:', error);
  }
}
```

### Пример 3: HTML элементы для отображения результатов

```html
<!DOCTYPE html>
<html>
<head>
    <title>Анализ таблицы</title>
    <style>
        .analysis-container {
            display: flex;
            gap: 20px;
            margin: 20px;
        }
        
        .analysis-block {
            flex: 1;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 15px;
            background-color: #f9f9f9;
        }
        
        .analysis-block h3 {
            margin-top: 0;
            color: #333;
        }
        
        .analysis-content {
            line-height: 1.6;
            color: #555;
        }
        
        .error {
            color: #d32f2f;
            background-color: #ffebee;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #3498db;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <h1>Анализ таблицы через AI</h1>
    
    <!-- Кнопка запуска анализа -->
    <button onclick="startTableAnalysis()">Анализировать первые 15 строк</button>
    <button onclick="analyzeTableCustom()">Анализировать первые 10 строк</button>
    
    <!-- Индикатор загрузки -->
    <div id="loading" style="display: none;" class="loading">
        <div class="spinner"></div>
        <p>Анализ данных...</p>
    </div>
    
    <!-- Блоки с результатами анализа -->
    <div class="analysis-container" id="results" style="display: none;">
        <!-- GigaChat -->
        <div class="analysis-block">
            <h3>📊 Анализ GigaChat</h3>
            <div class="analysis-content" id="giga-analysis">
                Ожидание результата...
            </div>
            <div id="giga-error" class="error" style="display: none;"></div>
        </div>
        
        <!-- Proxy API -->
        <div class="analysis-block">
            <h3>🤖 Анализ Proxy API</h3>
            <div class="analysis-content" id="proxy-analysis">
                Ожидание результата...
            </div>
            <div id="proxy-error" class="error" style="display: none;"></div>
        </div>
    </div>
    
    <script>
        async function startTableAnalysis() {
            await analyzeTableDefault();
        }
        
        async function analyzeTableDefault() {
            // Показываем загрузку
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
            try {
                const response = await fetch('/api/table-analysis', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({})
                });
                
                const data = await response.json();
                displayResults(data);
                
            } catch (error) {
                console.error('Ошибка при анализе:', error);
                document.getElementById('loading').style.display = 'none';
                alert('Ошибка при анализе: ' + error.message);
            }
        }
        
        async function analyzeTableCustom() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
            try {
                const response = await fetch('/api/table-analysis', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ rows_count: 10 })
                });
                
                const data = await response.json();
                displayResults(data);
                
            } catch (error) {
                console.error('Ошибка:', error);
                document.getElementById('loading').style.display = 'none';
                alert('Ошибка: ' + error.message);
            }
        }
        
        function displayResults(data) {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('results').style.display = 'flex';
            
            // GigaChat результат
            if (data.giga_result) {
                document.getElementById('giga-analysis').textContent = data.giga_result;
                document.getElementById('giga-error').style.display = 'none';
            } else if (data.errors.giga_chat) {
                document.getElementById('giga-analysis').textContent = '';
                document.getElementById('giga-error').textContent = '❌ Ошибка: ' + data.errors.giga_chat;
                document.getElementById('giga-error').style.display = 'block';
            }
            
            // Proxy API результат
            if (data.proxy_result) {
                document.getElementById('proxy-analysis').textContent = data.proxy_result;
                document.getElementById('proxy-error').style.display = 'none';
            } else if (data.errors.proxy_api) {
                document.getElementById('proxy-analysis').textContent = '';
                document.getElementById('proxy-error').textContent = '❌ Ошибка: ' + data.errors.proxy_api;
                document.getElementById('proxy-error').style.display = 'block';
            }
        }
    </script>
</body>
</html>
```

## Системный промпт (System Prompt)

При отправке в API используется следующий формат системного промпта:

```
Ты - аналитическая система с большим опытом. Твоя задача - анализировать табличные данные, делать выводы и находить аномалии или интересные тенденции.

Вот первые [N] строк таблицы:

[ТАБЛИЦА]

Проанализируй эти данные, выдели ключевые особенности, найди закономерности, аномалии и интересные тенденции. Предоставь краткий, но информативный анализ.
```

## Обработка ошибок

### Возможные ошибки и решения

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `No data loaded` | Файл не загружен | Загрузите файл через `/api/upload` |
| `GigaChat API not initialized` | Токен GigaChat не установлен | Проверьте `GIGACHAT_TOKEN` в `.env` |
| `Proxy API not initialized` | API ключ Proxy не установлен | Проверьте `PROXY_API_KEY` в `.env` |
| `Request timeout` | API не отвечает в отведенное время | Повторите запрос позже |
| `Invalid data type` | Некорректный формат данных | Убедитесь, что данные - DataFrame или список словарей |

## Тестирование

### Запуск тестов

```bash
cd d:\Курсор\DataAnalitics_AI-Flask
.\.venv\Scripts\python.exe test_table_analysis.py
```

### Включенные тесты

1. **test_analyze_table_first_rows_with_dataframe** - анализ DataFrame
2. **test_analyze_table_first_rows_with_list** - анализ списка словарей
3. **test_analyze_table_custom_rows_count** - анализ с пользовательским количеством строк
4. **test_error_handling** - обработка ошибок API
5. **test_invalid_data_type** - обработка некорректных типов данных

## Логирование

Все операции логируются в `logs/app.log`:

```
[INFO] TABLE ANALYSIS REQUEST RECEIVED
[INFO]   Rows count to analyze: 15
[INFO]   DataFrame size: 100 rows, 5 columns
[INFO]   🤖 Sending data to analysis service...
[INFO]   ✅ Analysis completed successfully
```

## Примеры использования в реальных сценариях

### Сценарий 1: Быстрая диагностика данных

```javascript
// При загрузке файла автоматически отправляем на анализ
function onFileUploaded() {
  analyzeTableDefault(); // Анализируем первые 15 строк
}
```

### Сценарий 2: Сравнительный анализ

```javascript
// Анализируем разные количества строк для сравнения
async function compareAnalysis() {
  const results = {};
  
  for (let rows of [5, 10, 15, 20]) {
    const response = await fetch('/api/table-analysis', {
      method: 'POST',
      body: JSON.stringify({ rows_count: rows })
    });
    results[rows] = await response.json();
  }
  
  // Сравниваем результаты
  visualizeComparison(results);
}
```

### Сценарий 3: Интеграция с аналитической панелью

```html
<div class="analytics-panel">
  <h2>Аналитика данных</h2>
  
  <!-- Исходные данные -->
  <div class="data-preview">
    <h3>Первые 15 строк</h3>
    <table id="data-table"><!-- таблица данных --></table>
  </div>
  
  <!-- AI анализ -->
  <div class="ai-analysis">
    <h3>AI Анализ</h3>
    <button onclick="runAnalysis()">Запустить анализ</button>
    <div id="analysis-results"></div>
  </div>
</div>
```

## Производительность

- **Время отклика API**: 3-10 секунд в зависимости от нагрузки
- **Максимальный размер таблицы**: 100 000+ строк
- **Поддерживаемые форматы**: CSV, Excel, PDF
- **Максимальное количество строк для анализа**: не ограничено (рекомендуется 5-50)

## Будущие улучшения

- [ ] Кеширование результатов анализа
- [ ] Сохранение истории анализа
- [ ] Параллельная обработка нескольких таблиц
- [ ] Расширенные опции форматирования промпта
- [ ] Интеграция с дополнительными AI моделями
- [ ] Экспорт результатов в PDF/Excel

---

**Версия документации:** 1.0  
**Дата обновления:** 27 ноября 2025  
**Автор:** AI Development Team
