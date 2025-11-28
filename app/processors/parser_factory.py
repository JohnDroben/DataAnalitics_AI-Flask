from app.processors.csv_parser import parse_csv
from app.processors.excel_parser import parse_excel
from app.processors.pdf_parser import parse_pdf
from ..utils.logger import logger


class FileParser:
    def __init__(self, file_type):
        self.file_type = file_type
        logger.debug(f"FileParser initialized for type: {file_type}")
        self.parser = self._get_parser()

    def _get_parser(self):
        logger.debug(f"  Getting parser for file type: {self.file_type}")
        if self.file_type == 'csv':
            logger.debug("  Parser selected: CSV")
            return parse_csv
        elif self.file_type in ['xls', 'xlsx']:
            logger.debug("  Parser selected: Excel")
            return parse_excel
        elif self.file_type == 'pdf':
            logger.debug("  Parser selected: PDF")
            return parse_pdf
        else:
            error_msg = f"Unsupported file type: {self.file_type}"
            logger.error(f"  ❌ {error_msg}")
            raise ValueError(error_msg)

    def parse(self, file_path):
        logger.info(f"Parsing file: {file_path} using {self.file_type} parser")
        try:
            result = self.parser(file_path)
            logger.info(f"✅ File parsed successfully")
            return result
        except Exception as e:
            logger.error(f"❌ Error parsing file: {type(e).__name__}: {e}", exc_info=True)
            raise


def get_parser(file_type: str) -> FileParser:
    logger.debug(f"get_parser called with type: {file_type}")
    return FileParser(file_type)
