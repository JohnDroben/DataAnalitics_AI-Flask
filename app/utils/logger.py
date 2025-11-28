import logging
import os
import sys
import io

def setup_logger(name=None):
    """Настройка логирования с выводом в консоль и файл"""
    logger = logging.getLogger(name or __name__)
    
    # Не добавляем handlers если они уже есть
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler для файла (UTF-8)
    os.makedirs('logs', exist_ok=True)
    log_path = 'logs/app.log'
    # Если старый файл существует, делаем бэкап, чтобы он не ломал чтение UTF-8
    try:
        if os.path.exists(log_path):
            from datetime import datetime
            bak_name = f"logs/app.log.bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.replace(log_path, bak_name)
    except Exception:
        pass
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler для консоли — обёртка, чтобы незаписываемые символы заменялись
    try:
        stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        stream = sys.stdout
    console_handler = logging.StreamHandler(stream)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Не передавать выше (чтобы избежать дублирования)
    logger.propagate = False
    
    return logger

# Получаем логгер
logger = setup_logger('dataanalytics')