from config_data.config import ALL_DEPARTMENTS
from typing import Tuple, Optional, Union


def get_updatable_departments(departments_list: Optional[Union[Tuple, str]] = None) -> Tuple:
    if isinstance(departments_list, str):
        departments_list = (departments_list,)
    if departments_list is None:
        return ALL_DEPARTMENTS
    return departments_list
