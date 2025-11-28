import os
from .logger import logger


def validate_file(file):
    logger.info(f"Validating file: {file.filename}")
    
    allowed_extensions = {'xlsx', 'xls', 'csv', 'pdf'}
    filename = file.filename
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    logger.debug(f"  Filename: {filename}")
    logger.debug(f"  Extension: {ext}")
    logger.debug(f"  Allowed extensions: {allowed_extensions}")

    if not filename:
        logger.error("  ❌ No filename provided")
        raise ValueError("Недопустимое имя файла")
    
    if ext not in allowed_extensions:
        logger.error(f"  ❌ Extension '{ext}' not allowed")
        raise ValueError("Недопустимый формат файла")

    file_size = file.content_length
    max_size = 10 * 1024 * 1024  # 10MB
    logger.debug(f"  File size: {file_size} bytes (max: {max_size} bytes)")
    
    if file_size > max_size:
        logger.error(f"  ❌ File exceeds size limit ({file_size} > {max_size})")
        raise ValueError("Файл превышает допустимый размер")

    logger.info("  ✅ File validation passed")
    return True