# 🔧 Отладка GigaChat API: 404 Error

## 🔴 Проблема

При запросе к GigaChat API возвращается **404 Not Found** ошибка.

## 🔍 Причины

1. **Неверный токен** - токен истек или неправильный формат
2. **Неверный URL** - API изменился или deprecated
3. **Неправильные заголовки** - отсутствует RqUID или другие требуемые headers
4. **Неправильная модель** - название модели не существует

## ✅ Решение

### Шаг 1: Проверьте токен

```bash
# Откройте .env файл
cat .env | grep GIGACHAT_TOKEN

# Токен должен быть в формате:
# GIGACHAT_TOKEN=<ваш_токен>
```

### Шаг 2: Получите новый токен

1. Откройте https://console.gigachat.ai/
2. Авторизуйтесь или создайте аккаунт
3. Перейдите в API Keys
4. Создайте новый API ключ
5. Скопируйте токен

### Шаг 3: Проверьте формат токена

Токен должен быть:
- ✅ Длиной 100+ символов
- ✅ Содержать буквы и цифры
- ✅ Не содержать пробелов
- ❌ НЕ начинаться с `Bearer`
- ❌ НЕ быть пустым

### Шаг 4: Обновите .env

```bash
# Правильно
GIGACHAT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Неправильно
GIGACHAT_TOKEN=Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
GIGACHAT_TOKEN=
GIGACHAT_TOKEN=test
```

### Шаг 5: Тестируйте OAuth получение токена

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('GIGACHAT_TOKEN')

print(f"Token length: {len(token)}")
print(f"Token starts with: {token[:20]}...")

# Пробуем получить access token
url = "https://auth.api.cloud.yandex.net/oauth/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
}
payload = f"grant_type=client_credentials&client_id={token}"

response = requests.post(url, headers=headers, data=payload, verify=False)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:300]}")
```

### Шаг 6: Проверьте доступность API

```bash
# Проверьте доступ к API
curl -X GET https://api.gigachat.ru/core/api/v1/models \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --insecure
```

## 📋 Альтернативные решения

### Вариант 1: Использовать mock режим для тестирования

```python
# В app/api/giga_chat.py добавьте:
USE_MOCK_RESPONSES = os.getenv('USE_MOCK_RESPONSES', 'false').lower() == 'true'

if USE_MOCK_RESPONSES:
    logger.warning("⚠️ Using mock responses for GigaChat API!")
    self.access_token = "mock_token"
```

### Вариант 2: Отключить GigaChat для тестирования

```bash
# В app/services/analysis_service.py в __init__:
try:
    self.giga_api = GigaChatAPI() if os.getenv('ENABLE_GIGACHAT', 'true').lower() == 'true' else None
except:
    self.giga_api = None
```

### Вариант 3: Использовать прокси API

Если GigaChat не работает, система автоматически перейдет на Proxy API.

## 🔍 Отладочная информация

### Логирование в режиме DEBUG

```bash
# Обновите logging.py
LOG_LEVEL=DEBUG

# Будут видны все детали запроса
```

### Проверка логов

```bash
# Смотрите последние 50 строк логов
tail -50 logs/app.log

# Или в Windows PowerShell
Get-Content logs/app.log -Tail 50

# Следите за логами в реальном времени
Get-Content logs/app.log -Tail 1 -Wait
```

### Типичные проблемы в логах

**Проблема:** `404 Not Found`
```
ERROR - ❌ GIGAChat error: <html><head><title>404 Not Found</title>
```
**Решение:** Проверьте URL и токен

**Проблема:** `No access token available`
```
ERROR - ❌ No access token available
```
**Решение:** Проверьте токен в .env и доступ к OAuth сервису

**Проблема:** `OAuth failed with status 400`
```
WARNING - OAuth failed with status 400: ...
```
**Решение:** Токен неверного формата, получите новый

## 🧪 Тестирование

### Запустите unit тесты с отладкой

```bash
# Добавьте DEBUG логирование
LOG_LEVEL=DEBUG .\.venv\Scripts\python.exe test_table_analysis.py
```

### Запустите интеграционный тест

```bash
LOG_LEVEL=DEBUG .\.venv\Scripts\python.exe test_table_analysis_integration.py
```

## 📞 Дополнительная помощь

### Контакты GigaChat Support

- 🌐 https://gigachat.ai/
- 📧 support@gigachat.ai
- 📖 https://gigachat.ai/docs

### Полезные ссылки

- [GigaChat API Documentation](https://gigachat.ai/docs)
- [OAuth 2.0 Flow](https://gigachat.ai/docs/oauth)
- [Available Models](https://gigachat.ai/docs/models)

## ✅ Чек-лист решения

- [ ] Проверил токен в .env
- [ ] Токен не пустой и не начинается с "Bearer"
- [ ] Получил новый токен если старый истек
- [ ] Проверил формат токена (100+ символов)
- [ ] Смотрел логи для деталей ошибки
- [ ] Тестировал OAuth получение токена
- [ ] Перезагрузил приложение (python run.py)
- [ ] Проверил доступ к https://api.gigachat.ru

---

## 🚀 Если ничего не помогает

1. **Используйте только Proxy API** - система автоматически перейдет на него если GigaChat недоступен
2. **Проверьте VPN/Firewall** - может быть заблокирован доступ к gigachat.ru
3. **Используйте mock режим** для разработки и тестирования
4. **Обратитесь в GigaChat Support** с описанием ошибки

---

**Дата:** 27 ноября 2025  
**Статус:** Рекомендации по отладке
