from utils.update_schedule import update_links, update_schedule
from utils.misc.add_department import add_department
from utils.misc.save_schedule import write_to_excel
from utils.updade_database.clear_database import clear_database
from utils.get_by import get_by_param


IS_WRITE_LOGS_TO_FILE: bool = False       # True >> Сохранять информацию о работе программы в log-файле
IS_WRITE_TO_CSW: bool = False   # True >> Сохранить результат поиска в data/<file_name>.csv

DEFAULT_COMMANDS = (
    ("Получить расписание соответствующее параметру", get_by_param),
    ("Сохранить в excel", write_to_excel),
    ("Внести изменения в индекс (добавить/удалить институт/факультет)", add_department),
    ("Обновить расписание групп", update_schedule),
    ("Обновить ссылки на расписание", update_links),
    ("Очистить базу данных", clear_database)
)
