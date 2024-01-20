from config_data.config import BASE_URL
from database.init_database import Schedule, Department, Group
from utils.updade_database.add_departments import add_departments
from utils.updade_database.add_groups import add_groups
from utils.updade_database.get_group_schedule import get_group_schedule
from utils.misc.log_writer import add_log

from typing import Tuple


def update_schedule(departments_to_update: Tuple, update_links: bool = False, is_full_update: bool = True) -> None:
    """ Обновление ссылок и расписаний групп """
    # Обновить ссылки на расписания ####################################################################################
    if update_links:
        if not is_full_update:
            if Department.select().count() == 0:
                add_departments(url=BASE_URL + "/schedule")
                add_log(log_message="Added links to departments", log_level="INFO")

            for i_department in Department.select():
                if i_department.department_name in departments_to_update:
                    Group.delete().where(Department.department_name == i_department.department_name).execute()
                    add_groups(url=BASE_URL + i_department.schedule_link, department=i_department.department_name)

        else:
            add_departments(url=BASE_URL + "/schedule")
            Group.delete().execute()
            for i_department in Department.select():
                if i_department.department_name in departments_to_update:
                    add_groups(url=BASE_URL + i_department.schedule_link, department=i_department.department_name)

    # Получить расписания групп ########################################################################################
    for i_department in departments_to_update:
        if is_full_update:
            Schedule.delete().execute()
        else:
            Schedule.delete().where(Group.department == i_department)

        total_classes = Schedule.select().count()
        add_log(log_message=f"total_classes -- {total_classes}", log_level="INFO")

        print(f"\n{i_department}:")
        for i_group in Group.select().where(Group.department == i_department):

            get_group_schedule(
                url=BASE_URL + i_group.schedule_link,
                department_name=i_department,
                group_number=i_group.group_number
            )

            add_log(log_message=f"total_classes -- {total_classes}", log_level="INFO")
            if total_classes > Schedule.select().count():
                total_classes = Schedule.select().count()
                add_log(log_message=f"Record is removed -- {i_department} -- {i_group.group_number} -- {total_classes}",
                        log_level="ERROR")
                raise ValueError(f"Record is removed -- {i_department} -- {i_group.group_number} -- {total_classes}")
