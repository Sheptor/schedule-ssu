import sys
from typing import Tuple, Callable
from utils.misc.init_logger import logger
from database.init_database import init_database


def main_loop(commands_list: Tuple[Tuple[str, Callable]]):
    """
    Обеспечение контроля ввода. Вводимый текст должен быть допустимой командой.
    """
    init_database()
    commands_list_text = "-"*20 + "\nСписок доступных команд:\n"
    commands_list_text += "\n".join("{} ---> {},".format(i, k[0]) for i, k in enumerate(commands_list, start=1))
    commands_list_text += "\n!stop ---> Завершить работу программы."
    commands_list_text += "\n" + "-"*20

    while True:
        logger.info(commands_list_text)
        command_number = input("Введите номер команды\n>>>").strip().lower()
        if command_number == "!stop":
            logger.info("__Script is completed__")
            sys.exit()
        try:
            command_number = int(command_number)
        except ValueError:
            logger.error(f"{command_number} -> Ввод не соответствует ни одному номеру команды.")
            continue
        if not 0 < command_number < len(commands_list) + 1:
            logger.error(f"{command_number} -> Ввод не соответствует ни одному номеру команды.")
            continue

        if len(commands_list[command_number - 1]) == 3:
            args = commands_list[command_number - 1][2]
            commands_list[command_number - 1][1](*args)
            continue

        commands_list[command_number - 1][1]()
