# DataAnalitics_AI-Flask

Короткое описание

- Flask-приложение для анализа табличных данных с использованием GigaChat (Sber) и опционального Proxy API.

Быстрый старт

1. Клонируйте репозиторий и создайте виртуальное окружение:

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

1. Создайте файл `.env` в корне проекта со следующими переменными (пример):

```text
GIGACHAT_CREDENTIALS=ваши_креды_или_ключ
# или
GIGACHAT_TOKEN=предварительно_полученный_токен

# Опционально: изменить endpoint
GIGACHAT_BASE_URL=https://gigachat.devices.sberbank.ru/api/v1
GIGACHAT_OAUTH_URL=https://ngw.devices.sberbank.ru:9443/api/v2/oauth

PROXY_API_KEY=ваш_proxy_api_key
PROXY_ENABLED=true
```

Важно: код по умолчанию использует `GIGACHAT_CREDENTIALS`/`GIGACHAT_TOKEN`. Если доступна библиотека `gigachat`, сервис попробует обменять креды на access token через SDK. Для разработки библиотека также запускается с `verify_ssl_certs=False` (НЕ использовать в production).

Session / история чата

- Для ускорения и повторного использования подсчитанных токенов GigaChat поддерживается `X-Session-ID`.
- В `AnalysisService` передаётся `session_id` (если есть) и он устанавливается в `gigachat.context.session_id_cvar` (при поддержке SDK).
- Передавайте `session_id` из вашего HTTP-эндпоинта (например, заголовок `X-Session-ID`) в вызовы анализатора.

Примеры запуска

- Запуск приложения:

```powershell
py run.py
```

Отладка и частые ошибки

- Если вы видите 404 или HTML-ответы от старого wrapper (`api.gigachat.ru`), задайте `GIGACHAT_BASE_URL` на официальный endpoint `https://gigachat.devices.sberbank.ru/api/v1` и используйте `GIGACHAT_CREDENTIALS`.
- DNS/NameResolutionError для `api.proxy.ai` означает, что ваша сеть не может резолвить адрес proxy — проверьте подключение, `hosts` и настройки прокси.
- Временное отключение валидации SSL (`verify=False`) включено только для разработки; в production включите проверку сертификатов.

Что изменено в коде

- `app/services/analysis_service.py`: добавлена поддержка `session_id`, установка `gigachat.context.session_id_cvar` и использование официальной библиотеки когда доступна.
- `app/api/giga_chat.py`: `GIGACHAT_BASE_URL` настраиваем, попытка получить access token через `gigachat` SDK, fallback на `GIGACHAT_TOKEN`.

Тесты

- Рекомендуется добавить unit‑тесты с моками для `gigachat` (проверка установки `session_id` в `gigachat.context`).

Безопасность

- Никогда не храните реальные креды в публичных репозиториях.
- Перед деплоем уберите `verify_ssl_certs=False` и используйте защищённое хранение секретов.

Контакты

- Поддержка: команда проекта (добавьте контакты по необходимости).
