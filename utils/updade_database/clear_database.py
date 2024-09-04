from utils.misc.init_logger import logger
from database.init_database import init_database, session, Schedule, Group, Base, engine


def clear_database():
    """ Удаление всех данных из базы данных. """
    confirm = input(f"Вы действительно хотите очистить базу данных?\n[y/n] >>>").lower()
    if confirm == "y":
        Base.metadata.drop_all(bind=engine)
        init_database()
        logger.warning("База данных очищена.")
    else:
        logger.warning("Отмена очистки.")
