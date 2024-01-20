import requests
import re

from config_data.config import DEPARTMENTS_PATTERN
from database.init_database import Department
from utils.misc.wait import wait


def add_departments(url: str) -> None:
    """
    Добавление ссылок на расписания институтов/факультетов.

    Arguments:
        url (str): URL станицы с расписанием университета

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
    ]
    Department.insert_many(departments_info).execute()
    print("Ссылки на расписания институтов/факультетов обновлены.")
    wait()
