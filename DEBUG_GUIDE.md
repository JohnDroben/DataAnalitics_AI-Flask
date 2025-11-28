# 🔧 Справка по отладке

Быстрая справка по решению проблем и отладке системы.

## ⚡ Быстрые команды

```bash
# Запустить с отладкой
LOG_LEVEL=DEBUG python run.py

# Запустить с mock API
USE_MOCK_API=true python run.py

# Просмотреть логи
Get-Content logs/app.log -Tail 50

# Следить за логами
Get-Content logs/app.log -Tail 1 -Wait

# Запустить тесты
.\.venv\Scripts\python.exe test_table_analysis.py

# Запустить интеграционные тесты
.\.venv\Scripts\python.exe test_table_analysis_integration.py
```

## 🔴 Частые ошибки и решения

### 1. GigaChat API 404 Error

**Симптомы:**
```
ERROR - ❌ GIGAChat error: <html><head><title>404 Not Found</title>
```

**Решения:**
1. Проверьте GIGACHAT_TOKEN в .env
2. Получите новый токен из https://gigachat.ai/
3. Используйте mock режим: `USE_MOCK_API=true`

📖 [Полная справка](GIGACHAT_DEBUG.md)

### 2. "No data loaded"

**Симптомы:**
```
{"status": "error", "message": "No data loaded"}
```

**Решения:**
1. Сначала загрузите файл: POST /api/upload
2. Выберите CSV, Excel или PDF
3. Потом вызовите /api/table-analysis

### 3. Timeout ошибки

**Симптомы:**
```
ERROR - ❌ GigaChat API request timeout
```

**Решения:**
1. API перегружена, повторите позже
2. Проверьте интернет соединение
3. Используйте mock режим для тестирования

### 4. SSL Certificate Error

**Симптомы:**
```
InsecureRequestWarning: Unverified HTTPS request is being made
```

**Это нормально!** Система временно отключила SSL проверку для разработки.

## 📊 Проверка статуса

### Статус приложения

```bash
# Проверьте что приложение запущено
curl http://localhost:3000/

# Получите информацию о данных
curl http://localhost:3000/api/data?limit=5
```

### Статус логирования

```bash
# Проверьте логирование работает
Get-Content logs/app.log -Tail 20

# Должны быть строки типа:
# INFO - Home page requested
# INFO - Data request received
```

### Статус API ключей

```python
import os
from dotenv import load_dotenv

load_dotenv()

gigachat_token = os.getenv('GIGACHAT_TOKEN')
proxy_api_key = os.getenv('PROXY_API_KEY')

print(f"GigaChat Token: {'✓' if gigachat_token else '✗'} ({len(gigachat_token or '')} chars)")
print(f"Proxy API Key: {'✓' if proxy_api_key else '✗'} ({len(proxy_api_key or '')} chars)")
```

## 🧪 Режимы тестирования

### Mock режим (для разработки)

```bash
# Включите mock
USE_MOCK_API=true python run.py

# Все запросы вернут mock результаты с префиксом [MOCK]
```

### Debug режим (для отладки)

```bash
# Включите debug логирование
LOG_LEVEL=DEBUG python run.py

# Будут видны все детали запросов
```

### Normal режим (production)

```bash
# Обычный режим с реальными API
python run.py
```

## 📝 Просмотр логов

### По уровню серьезности

```bash
# Только ошибки
Get-Content logs/app.log | Select-String "ERROR"

# Только предупреждения
Get-Content logs/app.log | Select-String "WARNING"

# Только информацию
Get-Content logs/app.log | Select-String "INFO"

# Только debug
Get-Content logs/app.log | Select-String "DEBUG"
```

### По времени

```bash
# Последний час
Get-Content logs/app.log | Select-String "$(Get-Date -f 'yyyy-MM-dd HH:')"

# Последние 5 минут
Get-Content logs/app.log -Tail 50
```

### По операции

```bash
# Анализ таблицы
Get-Content logs/app.log | Select-String "table.analysis|TABLE ANALYSIS"

# Загрузка файла
Get-Content logs/app.log | Select-String "upload|UPLOAD"

# API запросы
Get-Content logs/app.log | Select-String "GigaChat|Proxy"
```

## 🔍 Отладка конкретной проблемы

### Проблема: Анализ возвращает пустой результат

**Отладка:**
1. Проверьте логи: `Get-Content logs/app.log | Select-String "analyze_table"`
2. Посмотрите размер данных: `Get-Content logs/app.log | Select-String "data size"`
3. Проверьте ошибки API: `Get-Content logs/app.log | Select-String "ERROR"`

### Проблема: Медленный ответ API

**Отладка:**
1. Посмотрите время ответа: `Get-Content logs/app.log | Select-String "Response status"`
2. Проверьте timeout: смотрите в логах "timeout"
3. Используйте mock режим для быстрого тестирования

### Проблема: Неправильный формат ответа

**Отладка:**
1. Проверьте JSON: `curl http://localhost:3000/api/table-analysis`
2. Смотрите валидацию в логах: `Get-Content logs/app.log | Select-String "JSON|response"`
3. Проверьте структуру в коде: `app/main.py:table_analysis()`

## 🛠️ Инструменты отладки

### Curl для тестирования

```bash
# Загрузить файл
curl -X POST http://localhost:3000/api/upload \
  -F "file=@test.csv"

# Анализировать таблицу
curl -X POST http://localhost:3000/api/table-analysis \
  -H "Content-Type: application/json" \
  -d "{\"rows_count\": 15}"

# Получить данные
curl http://localhost:3000/api/data?limit=10
```

### Python для отладки

```python
from app.services.analysis_service import AnalysisService
import pandas as pd

service = AnalysisService()
df = pd.read_csv('test.csv')

try:
    results = service.analyze_table_first_rows(df, rows_count=5)
    print("GigaChat:", results['giga_result'])
    print("Proxy API:", results['proxy_result'])
    print("Errors:", results['errors'])
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
```

### PowerShell для отладки

```powershell
# Проверьте переменные окружения
Get-ChildItem env: | grep -E "GIGACHAT|PROXY"

# Запустите с debug
$env:LOG_LEVEL = "DEBUG"
python run.py
```

## 📋 Чек-лист отладки

- [ ] Проверил логи в logs/app.log
- [ ] Посмотрел уровень логирования (DEBUG/INFO/ERROR)
- [ ] Проверил API ключи в .env
- [ ] Протестировал с mock режимом
- [ ] Использовал curl для проверки endpoint'ов
- [ ] Запустил unit тесты
- [ ] Запустил интеграционные тесты
- [ ] Посмотрел документацию

## 🚀 Воспроизведение проблемы

### Шаг 1: Запустите с debug

```bash
LOG_LEVEL=DEBUG python run.py
```

### Шаг 2: Воспроизведите проблему

Выполните действия которые вызывают ошибку.

### Шаг 3: Соберите логи

```bash
Get-Content logs/app.log > debug.log
```

### Шаг 4: Анализируйте

Посмотрите error сообщения и trace back.

## 📞 Когда обращаться за помощью

Приготовьте:
1. Точное описание проблемы
2. Шаги воспроизведения
3. Сохраненные логи (logs/app.log)
4. Версия Python (.\.venv\Scripts\python.exe --version)
5. Содержимое .env (без секретов)

---

**Для более подробной информации смотрите:**
- [GIGACHAT_DEBUG.md](GIGACHAT_DEBUG.md) - отладка GigaChat
- [MOCK_API_GUIDE.md](MOCK_API_GUIDE.md) - использование mock API
- [QUICKSTART.md](QUICKSTART.md) - быстрый старт
- [TABLE_ANALYSIS_GUIDE.md](TABLE_ANALYSIS_GUIDE.md) - полное руководство

---

**Удачи в отладке! 🚀**
