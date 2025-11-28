import pdfplumber
from ..utils.logger import logger

def parse_pdf(file_path):
    logger.info(f"Parsing PDF file: {file_path}")
    try:
        logger.debug(f"  Opening PDF with pdfplumber...")
        text = ""
        with pdfplumber.open(file_path) as pdf:
            page_count = len(pdf.pages)
            logger.debug(f"  Total pages: {page_count}")
            for idx, page in enumerate(pdf.pages):
                logger.debug(f"  Extracting text from page {idx + 1}/{page_count}")
                text += page.extract_text()
        logger.info(f"  ✅ PDF parsed successfully")
        logger.debug(f"     Total text length: {len(text)} chars")
        return text
    except Exception as e:
        error_msg = f"Ошибка при чтении PDF: {str(e)}"
        logger.error(f"  ❌ {error_msg}", exc_info=True)
        raise ValueError(error_msg)