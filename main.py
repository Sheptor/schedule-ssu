from utils.misc.init_logger import logger
from utils.misc.execute_command import main_loop
from config_data.config import DEFAULT_COMMANDS


if __name__ == '__main__':
    logger.info("__Script is started__")
    main_loop(DEFAULT_COMMANDS)
    logger.info("__Script is completed__")
