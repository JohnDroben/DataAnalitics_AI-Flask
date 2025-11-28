# Логирование системы аналитики данных

## Обзор

В проект добавлено **полное логирование** всего процесса загрузки и анализа документов. Система логирует каждый шаг с указанием статуса и деталей выполнения.

## Структура логирования

### 1. **Файлы логов**
- Основной лог: `logs/app.log`
- Формат: `YYYY-MM-DD HH:MM:SS - logger_name - LEVEL - function:line - message`
- Пример: `2025-11-27 20:37:13 - dataanalytics - INFO - analyze_file:40 - Getting parser for extension: .csv`

### 2. **Уровни логирования**
- **DEBUG** - Детальная информация для отладки
- **INFO** - Основная информация о процессе
- **WARNING** - Предупреждения о потенциальных проблемах
- **ERROR** - Ошибки с трассировкой стека (exc_info=True)

## Логирование процесса загрузки файла

### Этап 1: Получение запроса (main.py - upload_file)
```
POST /api/upload
→ Content-Type проверяется
→ Файл получен
→ Размер файла логируется
```

### Этап 2: Валидация файла (file_handler.py - validate_file)
```
Проверка имени файла
Проверка расширения (.csv, .xlsx, .xls, .pdf)
Проверка размера (макс 10MB)
```

### Этап 3: Парсинг файла (processors/parser_factory.py)
```
Определение типа файла по расширению
Выбор парсера (CSV/Excel/PDF)
Парсинг с логированием прогресса
```

### Этап 4: Анализ файла (services/analysis_service.py)
```
Инициализация API сервисов (GigaChat, ProxyAPI)
Подготовка данных для анализа
Отправка запросов к AI API
Генерация отчетов
```

## Примеры логов

### Успешная загрузка CSV
```
2025-11-27 20:37:13 - dataanalytics - INFO - upload_file:28 - POST /api/upload received
2025-11-27 20:37:13 - dataanalytics - INFO - upload_file:31 - File received: data.csv
2025-11-27 20:37:13 - dataanalytics - INFO - upload_file:32 - Size: 1024 bytes
2025-11-27 20:37:13 - dataanalytics - INFO - file_handler:11 - Validating file: data.csv
2025-11-27 20:37:13 - dataanalytics - INFO - file_handler:20 - File validation passed
2025-11-27 20:37:13 - dataanalytics - INFO - parser_factory:28 - Parser selected: CSV
2025-11-27 20:37:13 - dataanalytics - INFO - csv_parser:5 - Parsing CSV file: uploads/data.csv
2025-11-27 20:37:13 - dataanalytics - INFO - csv_parser:9 - CSV parsed successfully
2025-11-27 20:37:13 - dataanalytics - DEBUG - csv_parser:10 - Shape: (100, 5)
2025-11-27 20:37:13 - dataanalytics - DEBUG - csv_parser:11 - Columns: ['Name', 'Age', 'Salary', 'Department', 'Status']
2025-11-27 20:37:13 - dataanalytics - INFO - analysis_service:65 - Data converted to string for API (length: 5234 chars)
2025-11-27 20:37:13 - dataanalytics - INFO - giga_chat:86 - Sending POST request to GigaChat API...
```

### Обработка ошибок
```
2025-11-27 20:37:19 - dataanalytics - ERROR - giga_chat:96 - Request failed: ConnectionError
Traceback:
  File "app/api/giga_chat.py", line 88, in send_analysis_request
    response = requests.post(url, headers=headers, json=payload, verify=False, timeout=30)
...
```

## Данные в логах

### Информация о файле
- Имя файла
- Размер в байтах
- Расширение файла
- Путь сохранения

### Информация об анализе
- Тип парсера
- Количество строк/столбцов (для CSV/Excel)
- Длина текста в символах (для PDF)
- Время отправки запроса к API
- Статус ответа API

### Информация об ошибках
- Тип ошибки (с полным квалифицированным именем)
- Сообщение об ошибке
- Полная трассировка стека вызовов

## Использование логов для отладки

### Найти все ошибки
```
grep "ERROR" logs/app.log
```

### Найти все запросы к API
```
grep "Sending POST request" logs/app.log
```

### Найти конкретный файл
```
grep "filename.csv" logs/app.log
```

### Проверить время обработки
```
grep "File analysis completed" logs/app.log
```

## Измененные файлы

1. **app/utils/logger.py** - Полная переработка системы логирования
2. **app/main.py** - Добавлены логи на каждый шаг загрузки
3. **app/services/analysis_service.py** - Логирование процесса анализа
4. **app/processors/parser_factory.py** - Логирование парсинга
5. **app/processors/csv_parser.py** - Логирование CSV парсинга
6. **app/processors/excel_parser.py** - Логирование Excel парсинга
7. **app/processors/pdf_parser.py** - Логирование PDF парсинга
8. **app/api/giga_chat.py** - Логирование запросов к GigaChat
9. **app/api/proxy_api.py** - Логирование запросов к ProxyAPI
10. **app/utils/file_handler.py** - Логирование валидации файлов
11. **run.py** - Логирование запуска приложения

## Тестирование логирования

Запустить тест полного процесса анализа:
```bash
python test_full_analysis.py
```

Результаты показывают:
- ✅ Все этапы загрузки логируются
- ✅ Все ошибки с полной информацией логируются
- ✅ Информация записывается одновременно в консоль и в файл
- ✅ Логи содержат полезную информацию для отладки
