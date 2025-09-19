import pdfplumber

def parse_pdf(file_path):
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        raise ValueError(f"Ошибка при чтении PDF: {str(e)}")