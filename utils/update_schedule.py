from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # noqa
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from . import DEPARTMENTS_IN_INDEX
from database.init_database import Schedule, Group
from utils.updade_database.get_group_schedule import get_group_schedule
from utils.misc.init_logger import logger
from utils.misc.get_status import Counter


BASE_URL: str = "https://www.sgu.ru"


# ####################################################################################
def update_links():
    """
    Обновить ссылки на расписание
    """
    logger.info("Обновление ссылок на расписание...")
    Group.delete().execute()
    driver = webdriver.Chrome()
    driver.get(BASE_URL + "/schedule")
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div/main/div[3]/div[2]/section[3]/div/div[2]/div[1]/div/div[2]/div/div')
            )
        )
        html = driver.page_source
    except TimeoutException:
        logger.error("Страница не загружается")
        return 1
    finally:
        driver.quit()
    soup = BeautifulSoup(html, "html.parser")
    departments_list = soup.find_all("div", {"class":"accordion__list"})
    groups = []
    for i_department in departments_list:
        i_department_name = i_department.find("h3", {"class":"accordion__header"}).text
        groups.extend([
            {
                "group_number": i_group.text,
                "schedule_link": i_group.attrs["href"],
                "department": i_department_name}
            for i_group in i_department.find_all("a", {"class": "schedule__group_item-link"})
        ])
    Group.insert_many(groups).execute()
    logger.info("Ссылки на расписание обновлены")


def update_schedule() -> None:
    """ Обновление ссылок и расписаний групп """
    logger.info("Обновление расписания...")
    # Удалить старое расписание ########################################################################################
    Schedule.delete().where(Group.department.in_(DEPARTMENTS_IN_INDEX))
    logger.warning("Расписание указанных факультетов/институтов очищено")

    # Получить расписания групп ########################################################################################
    counter = Counter()

    for i_department in DEPARTMENTS_IN_INDEX:
        logger.debug(f'Обновление расписания "{i_department}"...')
        counter.index_in_department = 0
        for i_group in Group.select().where(Group.department == i_department):

            get_group_schedule(
                url=BASE_URL + i_group.schedule_link,
                department_name=i_department,
                group_number=i_group.group_number
            )
            counter.current_group += 1
            counter.index_in_department += 1
            counter.get_status(department_name=i_department, group_number=i_group.group_number)
    logger.info("Расписание обновлено")