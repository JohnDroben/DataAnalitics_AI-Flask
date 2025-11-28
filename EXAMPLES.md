# 💡 Быстрые примеры использования

Готовые примеры для копирования и использования.

## 🚀 Запуск приложения

### Вариант 1: Обычный режим

```bash
python run.py
# Откроется http://localhost:3000
```

### Вариант 2: С отладкой

```bash
LOG_LEVEL=DEBUG python run.py
```

### Вариант 3: С mock API (для тестирования)

```bash
USE_MOCK_API=true python run.py
```

### Вариант 4: С обоими параметрами

```bash
USE_MOCK_API=true LOG_LEVEL=DEBUG python run.py
```

## 📤 Загрузка файла

### Curl

```bash
# Загрузить CSV файл
curl -X POST http://localhost:3000/api/upload \
  -F "file=@data.csv"

# Загрузить Excel
curl -X POST http://localhost:3000/api/upload \
  -F "file=@data.xlsx"

# Загрузить PDF
curl -X POST http://localhost:3000/api/upload \
  -F "file=@data.pdf"
```

### PowerShell

```powershell
$file = Get-Item "data.csv"
$response = Invoke-WebRequest -Method POST `
  -Uri "http://localhost:3000/api/upload" `
  -Form @{ file = $file }

$response.Content | ConvertFrom-Json | Out-Host
```

### Python

```python
import requests

with open('data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:3000/api/upload',
        files={'file': f}
    )

print(response.json())
```

### JavaScript

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('/api/upload', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data);
```

## 📊 Анализ таблицы

### Curl (по умолчанию 15 строк)

```bash
curl -X POST http://localhost:3000/api/table-analysis \
  -H "Content-Type: application/json" \
  -d "{}"
```

### Curl (пользовательское количество)

```bash
# Анализировать 10 строк
curl -X POST http://localhost:3000/api/table-analysis \
  -H "Content-Type: application/json" \
  -d "{\"rows_count\": 10}"

# Анализировать 25 строк
curl -X POST http://localhost:3000/api/table-analysis \
  -H "Content-Type: application/json" \
  -d "{\"rows_count\": 25}"

# Анализировать все строки (100)
curl -X POST http://localhost:3000/api/table-analysis \
  -H "Content-Type: application/json" \
  -d "{\"rows_count\": 100}"
```

### PowerShell

```powershell
# По умолчанию
$response = Invoke-RestMethod -Method POST `
  -Uri "http://localhost:3000/api/table-analysis" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body "{}"

# С параметрами
$response = Invoke-RestMethod -Method POST `
  -Uri "http://localhost:3000/api/table-analysis" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body @{ rows_count = 20 } | ConvertTo-Json

$response | Out-Host
```

### Python

```python
import requests

# По умолчанию
response = requests.post(
    'http://localhost:3000/api/table-analysis',
    json={}
)

# С параметрами
response = requests.post(
    'http://localhost:3000/api/table-analysis',
    json={'rows_count': 15}
)

data = response.json()
print("GigaChat:", data['giga_result'])
print("Proxy API:", data['proxy_result'])
if data['errors']:
    print("Errors:", data['errors'])
```

### JavaScript

```javascript
// По умолчанию
const response = await fetch('/api/table-analysis', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({})
});

// С параметрами
const response = await fetch('/api/table-analysis', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ rows_count: 20 })
});

const data = await response.json();
console.log("GigaChat:", data.giga_result);
console.log("Proxy API:", data.proxy_result);
console.log("Errors:", data.errors);
```

## 📈 Получение данных

### Curl

```bash
# Первые 10 строк
curl http://localhost:3000/api/data?offset=0&limit=10

# Строки 20-30
curl http://localhost:3000/api/data?offset=20&limit=10

# Все доступные строки
curl http://localhost:3000/api/data?offset=0&limit=1000
```

### PowerShell

```powershell
$data = Invoke-RestMethod -Method GET `
  -Uri "http://localhost:3000/api/data?offset=0&limit=15"

$data.rows | Format-Table -AutoSize
```

### Python

```python
import requests

response = requests.get(
    'http://localhost:3000/api/data',
    params={'offset': 0, 'limit': 15}
)

data = response.json()
print(f"Columns: {data['columns']}")
print(f"Total rows: {data['total_rows']}")
for row in data['rows']:
    print(row)
```

### JavaScript

```javascript
const response = await fetch('/api/data?offset=0&limit=15');
const data = await response.json();

console.log("Columns:", data.columns);
console.log("Total rows:", data.total_rows);
data.rows.forEach(row => console.log(row));
```

## 🧪 Тестирование

### Запуск всех тестов

```bash
# Unit тесты
.\.venv\Scripts\python.exe test_table_analysis.py

# Интеграционные тесты
.\.venv\Scripts\python.exe test_table_analysis_integration.py

# Оба сразу
.\.venv\Scripts\python.exe test_table_analysis.py && .\.venv\Scripts\python.exe test_table_analysis_integration.py
```

### Примеры API тестирования

```bash
# PowerShell примеры
.\test_table_analysis_api.ps1
```

## 📝 Полный рабочий процесс

### Шаг за шагом

```bash
# 1. Запустить приложение
python run.py

# 2. Загрузить файл (в новой консоли)
curl -X POST http://localhost:3000/api/upload \
  -F "file=@test.csv"

# 3. Получить данные
curl http://localhost:3000/api/data?limit=5

# 4. Анализировать таблицу
curl -X POST http://localhost:3000/api/table-analysis \
  -H "Content-Type: application/json" \
  -d "{\"rows_count\": 15}"

# 5. Смотреть результаты
Get-Content logs/app.log -Tail 20
```

## 🔧 Полезные команды

### Просмотр логов

```bash
# Последние 50 строк
Get-Content logs/app.log -Tail 50

# Следить в реальном времени
Get-Content logs/app.log -Tail 1 -Wait

# Только ошибки
Get-Content logs/app.log | Select-String "ERROR"

# Только информация
Get-Content logs/app.log | Select-String "INFO"
```

### Работа с файлами

```bash
# Список загруженных файлов
Get-ChildItem uploads/

# Список сгенерированных отчетов
Get-ChildItem reports/

# Создать тестовый CSV
@"
ID,Name,Value
1,Item1,100
2,Item2,200
3,Item3,300
"@ | Out-File test.csv
```

### Проверка окружения

```bash
# Проверить Python
python --version

# Проверить зависимости
pip list | grep -E "flask|pandas|requests"

# Проверить переменные окружения
dir env: | grep -E "GIGACHAT|PROXY|USE_MOCK"
```

## 💻 Примеры на разных языках

### Загрузка + анализ (Python)

```python
import requests
import time

# 1. Загрузить файл
with open('data.csv', 'rb') as f:
    upload = requests.post(
        'http://localhost:3000/api/upload',
        files={'file': f}
    )
print(f"Upload: {upload.json()}")

# 2. Подождать немного
time.sleep(1)

# 3. Анализировать
analysis = requests.post(
    'http://localhost:3000/api/table-analysis',
    json={'rows_count': 15}
)

result = analysis.json()
print(f"\nGigaChat: {result['giga_result']}")
print(f"Proxy API: {result['proxy_result']}")
print(f"Errors: {result['errors']}")
```

### Загрузка + анализ (JavaScript)

```javascript
async function analyzeFile() {
  // 1. Загрузить файл
  const formData = new FormData();
  formData.append('file', document.getElementById('file').files[0]);
  
  const upload = await fetch('/api/upload', {
    method: 'POST',
    body: formData
  });
  console.log('Upload:', await upload.json());
  
  // 2. Подождать
  await new Promise(r => setTimeout(r, 1000));
  
  // 3. Анализировать
  const analysis = await fetch('/api/table-analysis', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ rows_count: 15 })
  });
  
  const result = await analysis.json();
  console.log('GigaChat:', result.giga_result);
  console.log('Proxy API:', result.proxy_result);
}
```

### Загрузка + анализ (PowerShell)

```powershell
function Analyze-File {
  param([string]$FilePath)
  
  # 1. Загрузить файл
  $file = Get-Item $FilePath
  $upload = Invoke-WebRequest -Method POST `
    -Uri "http://localhost:3000/api/upload" `
    -Form @{ file = $file }
  Write-Host "Upload: $($upload.Content)"
  
  # 2. Подождать
  Start-Sleep -Seconds 1
  
  # 3. Анализировать
  $analysis = Invoke-RestMethod -Method POST `
    -Uri "http://localhost:3000/api/table-analysis" `
    -Headers @{ "Content-Type" = "application/json" } `
    -Body @{ rows_count = 15 } | ConvertTo-Json
  
  Write-Host "GigaChat: $($analysis.giga_result)"
  Write-Host "Proxy API: $($analysis.proxy_result)"
}

Analyze-File "test.csv"
```

## 🎯 Готовые сценарии

### Сценарий 1: Быстрый тест

```bash
# Mock режим, загрузить и анализировать
USE_MOCK_API=true python run.py &
sleep 2
curl -X POST http://localhost:3000/api/upload -F "file=@test.csv"
sleep 1
curl -X POST http://localhost:3000/api/table-analysis -H "Content-Type: application/json" -d "{}"
```

### Сценарий 2: Debug сессия

```bash
# Debug режим с mock API
USE_MOCK_API=true LOG_LEVEL=DEBUG python run.py
# Затем в другой консоли:
curl http://localhost:3000/api/data
```

### Сценарий 3: Production проверка

```bash
# Запустить тесты перед production
python test_table_analysis.py
python test_table_analysis_integration.py
# Если все ✅ - готово к развертыванию
```

---

**Готовые команды для копирования! 📋**
