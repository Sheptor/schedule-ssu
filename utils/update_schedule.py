from config_data.config import BASE_URL
from database.init_database import Schedule, Department, Group
from utils.add_departments import add_departments
from utils.add_groups import add_groups
from utils.get_group_schedule import get_group_schedule

from typing import Tuple


def update_schedule(departments_to_update: Tuple, update_links: bool = False) -> None:
    # Update links #####################################################################################################
    if update_links:
        add_departments(url=BASE_URL + "/schedule", departments_to_update=departments_to_update)

        # Get text from https://sgu.ru #################################################################################
        Group.delete().execute()
        for i_department in Department.select():
            add_groups(url=BASE_URL + i_department.schedule_link, department=i_department.department_name)
            print(f"Groups of {i_department.department_name} added.")

    # Get text from groups #############################################################################################
    for i_department in departments_to_update:
        print(f"\n{i_department}:")
        for i_group in Group.select().where(Group.department == i_department):
            get_group_schedule(
                url=BASE_URL + i_group.schedule_link,
                department_name=i_department,
                group_number=i_group.group_number
            )
