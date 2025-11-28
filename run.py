import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import main
from app.utils.logger import logger

if __name__ == '__main__':
    logger.info("=" * 80)
    logger.info("🚀 Starting Flask Application")
    logger.info("=" * 80)
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Python version: {sys.version}")
    logger.info("Starting server on http://0.0.0.0:3000")
    logger.info("=" * 80)
    
    try:
        main.app.run(host='0.0.0.0', port=3000, debug=True)
    except Exception as e:
        logger.error(f"❌ Failed to start application: {type(e).__name__}: {e}", exc_info=True)
        raise
