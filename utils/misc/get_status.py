from typing import Tuple
from database.init_database import Group
from peewee import fn


def get_timer(seconds_count: int) -> Tuple:
    """ Преобразование времени в секундах в формат h:m:s. """
    l_h = seconds_count // 3600
    l_m = (seconds_count - l_h * 3600) // 60
    l_s = seconds_count - (l_h * 3600 + l_m * 60)
    return l_h, l_m, l_s


def get_status(
        department_name,
        group_number
) -> None:
    """ Вывод информации о текущем статусе работы программы. """
    min_id = Group.select(fn.min(Group.group_id)).where(Group.department == department_name).scalar()
    current_group = Group.get(Group.department == department_name and Group.group_number == group_number)
    current_id = current_group.group_id
    index_in_department = current_id - min_id + 1

    total_in_department = Group.select().where(Group.department == department_name).count()
    department_percent = round(((index_in_department / total_in_department) * 100), 2)

    total_groups = Group.select().count()
    total_percent = round((current_id / total_groups) * 100, 2)

    total_time = (total_groups - current_id) * 50
    hours, minutes, seconds = get_timer(total_time)

    print(f"saved {department_name} {group_number}"
          f"\t\t\t{index_in_department}/{total_in_department}"
          f"({department_percent}%)"
          f"\t\t\t{current_id}/{total_groups} "
          f"({total_percent}%)"
          f"\t\t\ttime left: {hours}h:{minutes}m:{seconds}s")
