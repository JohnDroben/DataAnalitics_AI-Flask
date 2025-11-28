import pandas as pd
from ..utils.logger import logger

def parse_csv(file_path):
    logger.info(f"Parsing CSV file: {file_path}")
    try:
        logger.debug(f"  Reading CSV with pandas...")
        df = pd.read_csv(file_path)
        logger.info(f"  ✅ CSV parsed successfully")
        logger.debug(f"     Shape: {df.shape}")
        logger.debug(f"     Columns: {list(df.columns)}")
        return df
    except Exception as e:
        error_msg = f"Ошибка при чтении CSV: {str(e)}"
        logger.error(f"  ❌ {error_msg}", exc_info=True)
        raise ValueError(error_msg)