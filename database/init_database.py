from peewee import SqliteDatabase, Model, CharField, IntegerField, AutoField
import os
from config_data.config import WEEKDAYS_LIST

SCHEDULE_DB_PATH = os.path.join("database", "schedule.db")
schedule_db = SqliteDatabase(SCHEDULE_DB_PATH)


class BaseModel(Model):
    class Meta:
        database = schedule_db


class Department(BaseModel):
    department_id = IntegerField(primary_key=True)
    department_name = CharField()
    schedule_link = CharField()


class Group(BaseModel):
    group_id = IntegerField(primary_key=True)
    group_number = CharField()
    schedule_link = CharField()
    department = CharField()


class Schedule(BaseModel):
    day = CharField()
    time = CharField()
    department_name = CharField()
    group_number = CharField()
    even = CharField()
    class_type = CharField()
    name = CharField()
    teacher_name = CharField()
    room = CharField()
    other = CharField()

    def __str__(self) -> str:
        return (f"День недели: {self.day}, "
                f"Время: {self.time}, "
                f"Институт/факультет: {self.department_name}, "
                f"Группа: {self.group_number}, "
                f"Четность: {self.even}, "
                f"Тип (пр. лаб. лек.): {self.class_type} "
                f"Название предмета: {self.name}, "
                f"Преподаватель: {self.teacher_name}, "
                f"Аудитория: {self.room}, "
                f"Другое: {self.other}")


class Weekdays(BaseModel):
    id = AutoField(primary_key=True)
    day_name = CharField()


def init_database():
    """ Инициализация моделей """
    schedule_db.create_tables(BaseModel.__subclasses__())
    if Weekdays.select().count() == 0:
        Weekdays.insert_many(WEEKDAYS_LIST).execute()
