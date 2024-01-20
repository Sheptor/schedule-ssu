from typing import Tuple, Dict, List
import re

WRITE_LOGS: bool = False       # True >> Сохранять информацию о работе программы в log-файле
IS_WRITE_TO_CSW: bool = True   # True >> Сохранить результат поиска в data/<file_name>.csv

ALL_DEPARTMENTS: Tuple = (
    "Биологический факультет", "Географический факультет", "Геологический факультет",
    "Институт дополнительного профессионального образования", "Институт искусств",
    "Институт истории и международных отношений", "Институт физики", "Институт физической культуры и спорта",
    "Институт филологии и журналистики", "Институт химии", "Механико-математический факультет",
    "Социологический факультет", "Факультет иностранных языков и лингводидактики",
    "Факультет компьютерных наук и информационных технологий", "Факультет психологии",
    "Факультет психолого-педагогического и специального образования",
    "Факультет фундаментальной медицины и медицинских технологий", "Философский факультет", "Экономический факультет",
    "Юридический факультет", "Геологический колледж", "Колледж радиоэлектроники им. П.Н. Яблочкова",
    "Психолого-педагогический факультет", "Факультет математики и естественных наук", "Филологический факультет"
)

BASE_URL: str = "https://www.sgu.ru"

DEPARTMENTS_PATTERN = re.compile(r"<li><a href='(.+?)'>(.+?)</a></li>")
GROUPS_PATTERN = re.compile(r'<a href="(.+?)">(\d{3,4})</a>')

SUB_CLASS_PATTERN = re.compile(r"<div class='l l--t-\d l--r-\d l--g-\d'>(.+?</div></div>.+?)</div></div>")
EVEN_PATTERN = re.compile(r"alt='Чётность'>(.*?)</div>")
CLASS_TYPE_PATTERN = re.compile(r"alt='Тип'>(.*?)</div>")
CLASS_NAME_PATTERN = re.compile(r"<div class='l-dn'>(.*?)</div>")
TEACHER_NAME_PATTERN = re.compile(r"<div class='l-tn'>(<a href.+?>)?(.*?)(</a>)?</div>")
ROOM_PATTERN = re.compile(r"<div class='l-p'>(.*?)$")
OTHER_PATTERN = re.compile(r"alt='Другое'>(.*?)</div>")

CLASS_TO_TIME: Dict = {
    1: "08:20-09:50",
    2: "10:00-11:35",
    3: "12:05-13:40",
    4: "13:50-15:25",
    5: "15:35-17:10",
    6: "17:20-18:40",
    7: "18:45-20:05",
    8: "20:10-21:30",
}

WEEKDAYS_LIST: List[Dict] = [
    {"day_name": "Monday"},
    {"day_name": "Tuesday"},
    {"day_name": "Wednesday"},
    {"day_name": "Thursday"},
    {"day_name": "Friday"},
    {"day_name": "Saturday"},
    {"day_name": "Sunday"}
]
