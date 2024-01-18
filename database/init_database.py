from peewee import SqliteDatabase, Model, CharField, IntegerField, AutoField, ForeignKeyField
import os

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


def init_database():
    schedule_db.create_tables(BaseModel.__subclasses__())
