from peewee import SqliteDatabase, Model, CharField, IntegerField
import os

SCHEDULE_DB_PATH = os.path.join("database", "schedule.db")
schedule_db = SqliteDatabase(SCHEDULE_DB_PATH)


class BaseModel(Model):
    class Meta:
        database = schedule_db


class Group(BaseModel):
    group_id = IntegerField(primary_key=True)
    group_number = CharField()
    schedule_link = CharField()
    department = CharField()


class Schedule(BaseModel):
    weekday = CharField()
    time = CharField()
    practice = CharField()
    num = CharField()
    name = CharField()
    teacher = CharField()
    groups = CharField()
    room = CharField()
    other = CharField(null=True)
    weekday_id = IntegerField()

    class Meta:
        indexes = (
            (("weekday", "time", "num", "teacher"), True),
        )

    def __str__(self):
        return f"{self.weekday}, {self.time}, {self.practice}, {self.num}, {self.name}, {self.teacher}, {self.groups}, {self.room}, {self.other}"


def init_database():
    """ Инициализация моделей """
    schedule_db.create_tables(BaseModel.__subclasses__())
