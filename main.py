from utils.misc.init_logger import logger
from utils.misc.execute_command import main_loop
from config_data.config import DEFAULT_COMMANDS
from utils.get_by_params.get_by_group import get_by_group
from utils.misc.save_schedule import write_to_excel

from utils.update_schedule import update_schedule


if __name__ == '__main__':
    logger.info("__Script is started__")
    main_loop(DEFAULT_COMMANDS)
    logger.info("__Script is completed__")
