import requests
import re

from config_data.config import GROUPS_PATTERN
from utils.misc.wait import wait
from utils.misc.log_writer import add_log
from database.init_database import Group


def add_groups(url: str, department: str) -> None:
    """
    The function from the site provides a link to the schedule of classes
    of the institute group and returns a dictionary containing information
    about the link to the schedule of the group, the name of the file in
    which the information from the site is stored (None), the schedule
    of activities (None)

    Arguments:
        url (str): group schedule website URL
        department_name (str): name of the institute

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
    print(f"Groups of {department} added")
    wait()
