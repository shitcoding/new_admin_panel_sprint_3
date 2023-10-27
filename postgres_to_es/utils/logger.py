from loguru import logger
import sys

logger.add(
    'logs/etl_logs.log',
    rotation='20 MB',
    level='INFO',
)

logger.add(
    sys.stdout,
    level='INFO',
)
