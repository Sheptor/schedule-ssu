from loguru import logger
from config_data.config import IS_WRITE_LOGS_TO_FILE
import sys


logger.remove()
logger_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level}</level> | <level>{message}</level>"

if IS_WRITE_LOGS_TO_FILE:
    logger.add("logs/logs.log", format="{time} {level} {message}")
    logger.add(sink=sys.stdout, format=logger_format)
else:
    logger.add(sink=sys.stdout, format=logger_format)
