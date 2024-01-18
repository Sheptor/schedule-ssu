import requests
import re
from typing import Tuple

from config_data.config import DEPARTMENTS_PATTERN
from database.init_database import Department
from utils.wait import wait


def add_departments(url: str, departments_to_update: Tuple) -> None:
    """
    The function gets links to the schedule of institutes and faculties
    from the website and returns the dictionary {institute: link to schedule}

    Arguments:
        url (str): SSU schedule homepage website URL

    :return: None
    """
    Department.delete().execute()

    home_site_text = requests.get(url).text

    pattern = DEPARTMENTS_PATTERN

    department_to_link = re.findall(pattern, home_site_text)
    departments_info = [
        {"department_name": i_department,
         "schedule_link": i_link}
        for i_link, i_department in department_to_link
        if i_department in departments_to_update
    ]
    Department.insert_many(departments_info).execute()
    print("Departments added.")
    wait()
