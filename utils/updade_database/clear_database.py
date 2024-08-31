from utils.misc.init_logger import logger
from database.init_database import init_database, Schedule, Group


def clear_database():
    """ Удаление всех данных из базы данных. """
    confirm = input(f"Вы действительно хотите очистить базу данных?\n[y/n] >>>").lower()
    if confirm == "y":
        Group.drop_table()
        Schedule.drop_table()
        init_database()
        logger.warning("База данных очищена.")
    else:
        logger.warning("Отмена очистки.")
