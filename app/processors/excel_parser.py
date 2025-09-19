import pandas as pd

def parse_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        return df.to_string()
    except Exception as e:
        raise ValueError(f"Ошибка при чтении Excel: {str(e)}")

# app/processors/csv_parser.py
import pandas as pd

def parse_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df.to_string()
    except Exception as e:
        raise ValueError(f"Ошибка при чтении CSV: {str(e)}")

# app/processors/pdf_parser.py
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