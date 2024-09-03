from utils.misc.init_logger import logger
import requests
import sys
from bs4 import BeautifulSoup
from peewee import IntegrityError

from utils.misc.wait import wait
from database.init_database import Schedule


WEEKDAYS_LIST = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота")


def get_group_schedule(
        url: str,
        department_name: str,
        group_number: str) -> None:
    """
    Добавление расписания группы в базу данных.

    Arguments:
        url (str): URL страницы расписания группы
        department_name (str): Название института/факультета
        group_number (str): Номер группы

    :return: None
    """
    logger.debug(f'Получение расписания группы "{group_number}"...')

    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            logger.error(f"Ошибка получения ответа от сервера. Код ошибки: {response.status_code}.")
            wait()
            wait()
            response = requests.get(url, timeout=15)
            if response.status_code != 200:
                logger.critical(
                    f"После повторной отправки запроса, также возникла ошибка. Код ошибки: {response.status_code}."
                )
                raise Exception

    except requests.exceptions.Timeout:
        logger.error(f"Превышено время ожидания ответа от сервера.")
        wait()
        wait()
        try:
            response = requests.get(url, timeout=15)
            if response.status_code != 200:
                logger.critical(
                    f"После повторной отправки запроса, возникла ошибка. Код ошибки: {response.status_code}."
                )
                sys.exit(1)
        except requests.exceptions.Timeout:
            logger.critical(
                f"После повторной отправки запроса, время ожидания также было превышено."
            )
            sys.exit(1)

    soup = BeautifulSoup(response.text, "html.parser")

    group_schedule = []
    rows = soup.find_all("tr")
    for i_row in rows:
        time = i_row.find("div", {"class": "schedule-table__header"})
        if time is not None:
            time = time.text.strip().replace(" ", "").replace("\n\n", " - ")
            for j_index, j_lesson in enumerate(i_row.find_all("td")):
                for j_sub_lesson in j_lesson.find_all("div", {"class": "schedule-table__lesson"}):
                    properties = j_sub_lesson.find("div", {"class": "schedule-table__lesson-props"}).find_all("div")
                    practice = properties[0].text.strip()
                    if len(properties) == 2:
                        num = properties[1].text.strip()
                    else:
                        num = "Ч/З"
                    name = j_sub_lesson.find("div", {"class": "schedule-table__lesson-name"}).text.strip()
                    teacher = j_sub_lesson.find("div", {"class": "schedule-table__lesson-teacher"}).text.strip()
                    room = j_sub_lesson.find("div", {"class": "schedule-table__lesson-room"}).text.strip()
                    other = j_sub_lesson.find("div", {"class": "schedule-table__lesson-uncertain"}).text.strip()
                    if other == "":
                        other = None
                    group_schedule.append(
                        {
                            "weekday": WEEKDAYS_LIST[j_index],
                            "time": time,
                            "practice": practice,
                            "num": num,
                            "name": name,
                            "teacher": teacher,
                            "groups": group_number,
                            "room": room,
                            "other": other,
                            "weekday_id": j_index
                        }
                    )

    for i_lesson in group_schedule:
        try:
            Schedule.insert(i_lesson).execute()
        except IntegrityError:
            Schedule.update(
                groups=Schedule.groups + ", " + i_lesson["groups"]
            ).where(
                Schedule.weekday == i_lesson["weekday"],
                Schedule.time == i_lesson["time"],
                Schedule.num == i_lesson["num"],
                Schedule.practice == i_lesson["practice"],
                Schedule.teacher == i_lesson["teacher"],
                ~ Schedule.groups.contains(f"{i_lesson["groups"]}")
            ).execute()
    wait()

