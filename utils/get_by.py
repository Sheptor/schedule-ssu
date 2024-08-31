from utils.misc.init_logger import logger
from utils.get_by_params.get_by_room import get_by_room
from utils.get_by_params.get_by_teacher import get_by_teacher
from utils.get_by_params.get_by_group import get_by_group


PARAM_TO_FUNC = (
    ("Аудитория", get_by_room),
    ("Преподаватель", get_by_teacher),
    ("Группа", get_by_group)
)


def get_by_param() -> None:
    """
    Получение расписания занятий, соответствующих параметру.

    Arguments:
        param_name (str): По какому параметру проводить поиск
        param_value (str): Значение параметра
        is_write_to_csv (bool): True >> записать результат поиска в csv-файл

    :return: None
    """

    parameters_list_text = "-" * 20 + "\nСписок доступных параметров:\n"
    parameters_list_text += "\n".join("{} ---> {},".format(i, k[0]) for i, k in enumerate(PARAM_TO_FUNC, start=1))
    parameters_list_text += "\n!stop ---> Отмена поиска по параметру."
    parameters_list_text += "\n" + "-" * 20

    while True:
        logger.info(parameters_list_text)
        parameter = input("Введите номер параметра\n>>>").strip().lower()
        if parameter == "!stop":
            return
        try:
            parameter_number = int(parameter)
        except ValueError:
            logger.error(f"{parameter} -> Ввод не соответствует ни одному номеру параметра.")
            continue
        if not 0 < parameter_number < len(PARAM_TO_FUNC) + 1:
            logger.error(f"{parameter_number} -> Ввод не соответствует ни одному номеру параметра.")
            continue

        func = PARAM_TO_FUNC[parameter_number - 1][1]
        param_value = input("Введите значение параметра\n>>>")

        func(param_value)
        return
