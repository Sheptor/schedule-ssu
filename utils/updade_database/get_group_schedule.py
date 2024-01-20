import requests
import re
from utils.misc.get_status import get_status
from utils.misc.wait import wait
from config_data.config import (CLASS_TO_TIME, SUB_CLASS_PATTERN, EVEN_PATTERN, CLASS_TYPE_PATTERN, CLASS_NAME_PATTERN,
                                TEACHER_NAME_PATTERN, ROOM_PATTERN, OTHER_PATTERN)
from database.init_database import Schedule


def get_group_schedule(
        url: str,
        department_name: str,
        group_number: str) -> None:
    """
    Добавление расписания группы в базу данных.

    Arguments:
        url (str): URL страницы расписания группы
        department_name (str): Название института/факультета
        group_number (str): Номер группы

    :return: None
    """

    def is_none(var, index=1):
        if var is not None:
            return var[index]
        else:
            return "---"

    site_text = requests.get(url).text

    for i_day_index, i_day in enumerate(("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"), start=1):
        pattern = r"<td  id='\d_" + str(i_day_index) + "' class=''>(.*?)</td>"
        day_list = re.findall(pattern, site_text)
        for j_lesson_index, j_lesson in enumerate(day_list, start=1):
            sub_class = re.findall(SUB_CLASS_PATTERN, j_lesson)

            for k_sub_class in sub_class:
                class_time = CLASS_TO_TIME[j_lesson_index]
                even = is_none(re.search(EVEN_PATTERN, k_sub_class))
                class_type = is_none(re.search(CLASS_TYPE_PATTERN, k_sub_class))
                class_name = is_none(re.search(CLASS_NAME_PATTERN, k_sub_class))
                teacher = is_none(re.search(TEACHER_NAME_PATTERN, k_sub_class),
                                  index=2)
                room = is_none(re.search(ROOM_PATTERN, k_sub_class))
                other = is_none(re.search(OTHER_PATTERN, k_sub_class))
                Schedule.create(
                    day=i_day,
                    time=class_time,
                    department_name=department_name,
                    group_number=group_number,
                    even=even,
                    class_type=class_type,
                    name=class_name,
                    teacher_name=teacher,
                    room=room,
                    other=other
                )
    get_status(
        department_name=department_name,
        group_number=group_number)
    wait()

