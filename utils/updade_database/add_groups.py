import requests
import re

from config_data.config import GROUPS_PATTERN
from utils.misc.wait import wait
from utils.misc.log_writer import add_log
from database.init_database import Group


def add_groups(url: str, department: str) -> None:
    """
    Добавление ссылок на расписания групп.

    Arguments:
        url (str): URL расписания группы
        department_name (str): Название института/факультета

    :return: None
    """

    site_text = requests.get(url).text
    group_to_link = re.findall(GROUPS_PATTERN, site_text)

    groups_info = [
        {"group_number": i_group,
         "schedule_link": i_link,
         "department": department}
        for i_link, i_group in group_to_link]
    Group.insert_many(groups_info).execute()
    add_log(log_message=f"Groups of {department} added", log_level="INFO")
    print(f"Ссылки на расписания групп {department} обновлены")
    wait()
