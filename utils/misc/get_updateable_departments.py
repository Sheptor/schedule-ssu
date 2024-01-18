from config_data.config import ALL_DEPARTMENTS
from typing import Tuple, Optional


def get_updatable_departments(departments_list: Optional[Tuple] = None) -> Tuple:
    if departments_list is None:
        return ALL_DEPARTMENTS
    return departments_list
