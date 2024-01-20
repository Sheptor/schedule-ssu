from utils.get_by_params.get_by_room import get_by_room
from utils.get_by_params.get_by_teacher import get_by_teacher
from utils.get_by_params.get_by_group import get_by_group

PARAM_TO_FUNC = {
    "room": get_by_room,
    "teacher": get_by_teacher,
    "group": get_by_group
}


def get_by_param(param_name: str, param_value: str, is_write_to_csv: bool = False) -> None:
    """
    Получение расписания занятий, соответствующих параметру.

    Arguments:
        param_name (str): По какому параметру проводить поиск
        param_value (str): Значение параметра
        is_write_to_csv (bool): True >> записать результат поиска в csv-файл

    :return: None
    """
    func = PARAM_TO_FUNC.get(param_name)
    if func is None:
        print("Доступные параметры для поиска: `room`, `teacher`, `group`")
    func(param_value, is_write_to_csv=is_write_to_csv)
