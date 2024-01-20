import csv
import os
from peewee import ModelSelect


def write_to_csv(param_name: str, param_value: str, data: ModelSelect) -> None:
    """ Запись полученного расписания в csv-файл. """
    file_name = os.path.join("data", f"{param_name}_is_{param_value}.csv")
    print(f"\nWriting to {file_name} ...")
    with open(file_name, "w", encoding="utf-8", newline='') as file:
        csv_out = csv.writer(file)
        headers = ("День недели", "Время", "Институт/факультет", "Группа", "Четность", "Тип (пр. лаб. лек.)",
                   "Название предмета", "Преподаватель", "Аудитория", "Другое")
        csv_out.writerow(headers)
        for row in data:
            csv_out.writerow(row[1:])
