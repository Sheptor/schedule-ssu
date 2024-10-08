import utils
from utils.misc.init_logger import logger
from copy import copy


DEPARTMENTS_LIST = [
    "Биологический факультет", "Географический факультет", "Геологический факультет",
    "Институт дополнительного профессионального образования", "Институт истории и международных отношений",
    "Институт физики", "Институт филологии и журналистики", "Институт химии",
    "Механико-математический факультет", "Социологический факультет",
    "Факультет гуманитарных дисциплин, русского и иностранного языков (ПИ)",
    "Факультет иностранных языков и лингводидактики", "Факультет искусств (ПИ)",
    "Факультет компьютерных наук и информационных технологий", "Факультет психологии",
    "Факультет психолого-педагогического и специального образования (ПИ)",
    "Факультет физико-математических и естественно-научных дисциплин (ПИ)",
    "Факультет физической культуры и спорта (ПИ)", "Факультет фундаментальной медицины и медицинских технологий",
    "Философский факультет", "Экономический факультет", "Юридический факультет",
    "Геологический колледж", "Колледж радиоэлектроники им. П.Н. Яблочкова"
]


def add_department():
    departments_list_text = "-"*20 + "\nСписок доступных институтов/факультетов:\n"
    departments_list_text += "\n".join("{} ---> {},".format(*k) for k in enumerate(DEPARTMENTS_LIST, start=1))
    departments_list_text += "\n!all ---> Добавить всё/очистить индекс"
    departments_list_text += "\n!stop ---> Завершить добавление в индекс."
    departments_list_text += "\n" + "-"*20

    while True:
        logger.info(departments_list_text)
        department = input("Введите номер института/факультета\n>>>").strip().lower()
        if department == "!stop":
            return
        if department == "!all":
            if DEPARTMENTS_LIST == utils.DEPARTMENTS_IN_INDEX:
                utils.DEPARTMENTS_IN_INDEX = list()
                logger.info(f"Все факультеты и институты удалены из индекса.")
            else:
                utils.DEPARTMENTS_IN_INDEX = copy(DEPARTMENTS_LIST)
                logger.info(f"Все факультеты и институты добавлены в индекс.")
            continue
        try:
            department_number = int(department)
        except ValueError:
            logger.error(f"{department} -> Ввод не соответствует ни одному номеру института/факультета.")
            continue
        if not 0 < department_number < len(DEPARTMENTS_LIST) + 1:
            logger.error(f"{department_number} -> Ввод не соответствует ни одному номеру института/факультета.")
            continue

        department = DEPARTMENTS_LIST[department_number - 1]
        if department in utils.DEPARTMENTS_IN_INDEX:
            utils.DEPARTMENTS_IN_INDEX.remove(department)
            logger.info(f"{department} удален из индекса. Сейчас в индексе: ({utils.DEPARTMENTS_IN_INDEX})")
        else:
            utils.DEPARTMENTS_IN_INDEX.append(department)
            logger.info(f"{department} добавлен в индекс. Сейчас в индексе: ({utils.DEPARTMENTS_IN_INDEX})")