from typing import Tuple
from database.init_database import Group
from utils import DEPARTMENTS_IN_INDEX
from utils.misc.init_logger import logger


class Counter:
    def __init__(self):
        self.current_group: int = 0
        self.index_in_department = 0
        self.total_groups: int = Group.select().where(Group.department.in_(DEPARTMENTS_IN_INDEX)).count()
        self.__max_wait_time = 40


    @staticmethod
    def get_timer(seconds_count: int) -> Tuple:
        """ Преобразование времени в секундах в формат h:m:s. """
        l_h = seconds_count // 3600
        l_m = (seconds_count - l_h * 3600) // 60
        l_s = seconds_count - (l_h * 3600 + l_m * 60)

        return l_h, l_m, l_s

    def get_status(
            self,
            department_name,
            group_number
    ) -> None:
        """ Вывод информации о текущем статусе работы программы. """

        total_in_department = Group.select().where(Group.department == department_name).count()
        department_percent = round(((self.index_in_department / total_in_department) * 100), 2)

        total_percent = round((self.current_group / self.total_groups) * 100, 2)

        total_time = (self.total_groups - self.current_group) * self.__max_wait_time
        hours, minutes, seconds = self.get_timer(total_time)

        logger.debug(f'Расписание группы "{department_name} {group_number}" получено, '
                     f'\t\t\t{self.index_in_department}/{total_in_department} '
                     f'({department_percent}%)'
                     f'\t\t\t{self.current_group}/{self.total_groups} '
                     f'({total_percent}%)'
                     f'\t\t\tосталось времени: {hours}h:{minutes}m:{seconds}s')
