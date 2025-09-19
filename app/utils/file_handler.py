import os


def validate_file(file):
    allowed_extensions = {'xlsx', 'xls', 'csv', 'pdf'}
    filename = file.filename
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

    if not filename or ext not in allowed_extensions:
        raise ValueError("Недопустимый формат файла")

    if file.content_length > 10 * 1024 * 1024:  # 10MB
        raise ValueError("Файл превышает допустимый размер")

    return True