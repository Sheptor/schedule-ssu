from loguru import logger
from config_data.config import WRITE_LOGS

logger.add("logs/logs.log", format="{time} {level} {message}")


def add_log(log_message: str, log_level: str) -> None:
    if WRITE_LOGS:
        if log_level == "ERROR":
            logger.error(log_message)
        elif log_level == "INFO":
            logger.info(log_message)
        else:
            logger.debug("log_message")
