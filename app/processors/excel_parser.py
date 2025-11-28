import pandas as pd
from ..utils.logger import logger

def parse_excel(file_path):
    logger.info(f"Parsing Excel file: {file_path}")
    try:
        logger.debug(f"  Reading Excel with pandas...")
        df = pd.read_excel(file_path)
        logger.info(f"  ✅ Excel parsed successfully")
        logger.debug(f"     Shape: {df.shape}")
        logger.debug(f"     Columns: {list(df.columns)}")
        return df
    except Exception as e:
        error_msg = f"Ошибка при чтении Excel: {str(e)}"
        logger.error(f"  ❌ {error_msg}", exc_info=True)
        raise ValueError(error_msg)