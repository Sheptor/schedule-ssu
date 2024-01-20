from database.init_database import init_database, Schedule, Weekdays
from utils.update_schedule import update_schedule
from utils.clear_database import clear_database
from utils.get_by import get_by_param
from utils.misc.get_updateable_departments import get_updatable_departments
from utils.misc.log_writer import add_log
from config_data.config import IS_WRITE_TO_CSW


if __name__ == '__main__':
    add_log(log_message="__Script is started__", log_level="INFO")
    # Параметры ########################################################################################################
    DEPARTMENTS_TO_UPDATE = ("Институт физики",)  # Обновить только расписание Института физики
    # DEPARTMENTS_TO_UPDATE = None                # Обновить расписание всего университета

    CLEAR_DATABASE: bool = True    # True >> Удалить все данные из базы данных
    UPDATE_DATABASE: bool = True   # False >> Пропустить обновления базы данных игнорируя UPDATE_LINKS и IS_FULL_UPDATE
    UPDATE_LINKS: bool = True      # True >> Обновить ссылки на расписание (институтов/факультетов и групп)
    IS_FULL_UPDATE: bool = True    # True >> Обновить все ссылки или только те, что указаны в DEPARTMENTS_TO_UPDATE

    departments_to_update = get_updatable_departments(DEPARTMENTS_TO_UPDATE)
    init_database()

    # Очистить базу данных #############################################################################################
    if CLEAR_DATABASE:
        clear_database()

    # Обновить ссылки и расписания групп ###############################################################################
    if UPDATE_DATABASE:
        update_schedule(
            update_links=UPDATE_LINKS,
            departments_to_update=departments_to_update,
            is_full_update=IS_FULL_UPDATE
        )

    # Поиск занятий по параметрам ######################################################################################
    get_by_param(param_name="room", param_value="<ROOM>", is_write_to_csv=IS_WRITE_TO_CSW)
    get_by_param(param_name="teacher", param_value="<ИМЯ ПРЕПОДАВАТЕЛЯ>", is_write_to_csv=IS_WRITE_TO_CSW)
    get_by_param(param_name="group", param_value="<НОМЕР ГРУППЫ>", is_write_to_csv=IS_WRITE_TO_CSW)

    # Сообщения об окончании работы программы ##########################################################################
    add_log(log_message="__Script is completed__", log_level="INFO")
    print()
    print("=" * 40)
    print("The End!")
    print("=" * 40)
