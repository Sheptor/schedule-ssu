import requests
import re
from utils.get_status import get_status
from utils.wait import wait
from config_data.config import CLASS_TO_TIME
from database.init_database import Schedule


def get_group_schedule(
        url: str,
        department_name: str,
        group_number: str) -> None:
    """
    The function adds the name of the group schedule file
    and the group schedule to the schedule dictionary

    Arguments:
        url (str): group schedule website URL
        department_name (str): name of the institute
        group_number (str): group number
        current_group_index (int): index of the group in the entire list
        group_in_department_index (int): index of the group in the institute list

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
            sub_class = re.findall(
                r"<div class='l l--t-\d l--r-\d l--g-\d'>(.+?</div></div>.+?)</div></div>", j_lesson)

            for k_sub_class in sub_class:
                class_time = CLASS_TO_TIME[j_lesson_index]
                even = is_none(re.search(r"alt='Чётность'>(.*?)</div>", k_sub_class))
                class_type = is_none(re.search(r"alt='Тип'>(.*?)</div>", k_sub_class))
                class_name = is_none(re.search(r"<div class='l-dn'>(.*?)</div>", k_sub_class))
                teacher = is_none(re.search(r"<div class='l-tn'>(<a href.+?>)?(.*?)(</a>)?</div>", k_sub_class),
                                  index=2)
                room = is_none(re.search(r"<div class='l-p'>(.*?)$", k_sub_class))
                Schedule.create(
                    day=i_day,
                    time=class_time,
                    department_name=department_name,
                    group_number=group_number,
                    even=even,
                    class_type=class_type,
                    name=class_name,
                    teacher_name=teacher,
                    room=room
                )
    get_status(
        department_name=department_name,
        group_number=group_number)
    wait()

