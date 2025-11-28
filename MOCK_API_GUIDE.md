# 🧪 Mock режим для тестирования

При разработке часто нужно тестировать без реальных API запросов. Вот как настроить mock режим.

## 📋 Проблема

- Реальные API могут быть недоступны или платные
- 404 ошибки от GigaChat
- Медленное тестирование с реальными запросами

## ✅ Решение

### Способ 1: Использовать переменную окружения

Добавьте в `.env` файл:

```
USE_MOCK_API=true
```

### Способ 2: Создать mock версию сервиса

Создайте файл `app/services/mock_analysis_service.py`:

```python
import pandas as pd
from ..utils.logger import logger

class MockAnalysisService:
    def __init__(self):
        logger.info("Initializing MockAnalysisService")
        self.giga_api = MockGigaChatAPI()
        self.proxy_api = MockProxyAPI()

    def analyze_table_first_rows(self, data, rows_count=15):
        logger.info(f"[MOCK] Analyzing {rows_count} rows")
        
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = data
        
        first_rows = df.head(rows_count)
        table_str = first_rows.to_string(index=False)
        
        return {
            "giga_result": f"[MOCK GigaChat] Анализ {len(first_rows)} строк: {table_str[:100]}...",
            "proxy_result": f"[MOCK Proxy API] Быстрый анализ: {len(first_rows)} строк содержат данные",
            "errors": {}
        }

class MockGigaChatAPI:
    def send_analysis_request(self, data):
        logger.debug("[MOCK] Sending to GigaChat")
        return "[MOCK] Результат анализа от GigaChat. В данных видны интересные тренды."

class MockProxyAPI:
    def send_analysis_request(self, data):
        logger.debug("[MOCK] Sending to Proxy API")
        return "[MOCK] Результат анализа от Proxy API. Данные хорошо структурированы."
```

### Способ 3: Использовать в app/main.py

Обновите инициализацию сервиса:

```python
import os
from .services.analysis_service import AnalysisService
from .services.mock_analysis_service import MockAnalysisService

USE_MOCK_API = os.getenv('USE_MOCK_API', 'false').lower() == 'true'

if USE_MOCK_API:
    logger.warning("⚠️ Using MOCK API for testing!")
    analysis_service = MockAnalysisService()
else:
    analysis_service = AnalysisService()
```

## 🧪 Тестирование с Mock API

### Запустите с mock режимом

```bash
# Windows PowerShell
$env:USE_MOCK_API = "true"
python run.py

# Linux/Mac
export USE_MOCK_API=true
python run.py
```

### Тестируйте анализ

```bash
# Загрузите файл как обычно
curl -X POST http://localhost:3000/api/upload \
  -F "file=@test.csv"

# Отправьте на анализ
curl -X POST http://localhost:3000/api/table-analysis \
  -H "Content-Type: application/json" \
  -d "{\"rows_count\": 15}"

# Получите результаты с [MOCK] префиксом
```

## 📝 Примеры mock результатов

### Запрос
```json
{
  "rows_count": 15
}
```

### Ответ
```json
{
  "status": "success",
  "giga_result": "[MOCK GigaChat] Анализ 15 строк: ID  Name     Value...",
  "proxy_result": "[MOCK Proxy API] Быстрый анализ: 15 строк содержат данные",
  "errors": {}
}
```

## 🔄 Переключение между режимами

### Проверьте текущий режим в логах

Логи показывают:
- Реальный режим: `Initializing GigaChatAPI` и `Initializing ProxyAPI`
- Mock режим: `Initializing MockAnalysisService`

### Быстрое переключение

```bash
# Включить mock
echo USE_MOCK_API=true >> .env

# Отключить mock
echo USE_MOCK_API=false >> .env

# Или удалить
$env:USE_MOCK_API = $null
```

## 💡 Когда использовать mock

✅ **Используйте mock для:**
- Разработки UI (быстрые тесты)
- Unit тестирования сервиса
- CI/CD pipelines
- Демонстрации функциональности
- Локальной разработки без API ключей

❌ **Не используйте mock для:**
- Production deployment
- Integration тестирования с реальными данными
- Проверки качества AI анализа
- Production мониторинга

## 🧩 Расширение mock сервиса

### Добавьте более реалистичные результаты

```python
import random

class MockGigaChatAPI:
    def send_analysis_request(self, data):
        templates = [
            "Анализ показывает растущий тренд с корреляцией 0.87",
            "В данных обнаружена сезонность с периодом 7 дней",
            "Выявлены 3 аномалии в строках 5, 12 и 18",
            "Среднее значение: 145.3, стандартное отклонение: 23.5"
        ]
        return f"[MOCK] {random.choice(templates)}"
```

### Добавьте задержку для реалистичности

```python
import time

class MockGigaChatAPI:
    def send_analysis_request(self, data):
        time.sleep(2)  # Имитируем сетевую задержку
        return "[MOCK] Результат после 2 секунд ожидания"
```

### Добавьте обработку ошибок

```python
class MockGigaChatAPI:
    def __init__(self, fail_rate=0.1):
        self.fail_rate = fail_rate
    
    def send_analysis_request(self, data):
        import random
        if random.random() < self.fail_rate:
            raise Exception("[MOCK] Симулируем ошибку API")
        return "[MOCK] Успешный результат"
```

## 🔧 Продвинутая конфигурация

### Файл `app/config/mock_settings.py`

```python
# Mock конфигурация
MOCK_RESPONSES = {
    'giga_chat': [
        "Анализ показывает...",
        "В данных видны...",
        "Выявлены аномалии..."
    ],
    'proxy_api': [
        "Быстрый анализ...",
        "Данные структурированы...",
        "Тренд показывает..."
    ]
}

MOCK_DELAYS = {
    'giga_chat': 2,  # секунды
    'proxy_api': 1
}

MOCK_ERROR_RATE = 0.05  # 5% ошибок
```

## ✅ Чек-лист

- [ ] Добавил USE_MOCK_API в .env
- [ ] Создал mock_analysis_service.py
- [ ] Обновил app/main.py для использования mock
- [ ] Протестировал с mock режимом
- [ ] Проверил логи для подтверждения mock
- [ ] Добавил расширенные mock результаты

---

**Mock режим готов к использованию!** 🎉
