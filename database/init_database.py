from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.orm import Mapped, declarative_base, sessionmaker, mapped_column
import os
from config_data import BASE_DIR

SCHEDULE_DB_PATH = os.path.join(BASE_DIR, "database", "schedule.db")
engine = create_engine(f"sqlite:///{SCHEDULE_DB_PATH}")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Group(Base):
    __tablename__ = "groups"
    group_id: Mapped[int] = mapped_column(primary_key=True)
    group_number: Mapped[str] = mapped_column()
    schedule_link: Mapped[str] = mapped_column()
    department: Mapped[str] = mapped_column()


class Schedule(Base):
    __tablename__ = "schedule"
    id: Mapped[int] = mapped_column(primary_key=True)
    weekday: Mapped[str] = mapped_column()
    time: Mapped[str] = mapped_column()
    practice: Mapped[str] = mapped_column()
    num: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    teacher: Mapped[str] = mapped_column()
    groups: Mapped[str] = mapped_column()
    room: Mapped[str] = mapped_column()
    other: Mapped[str] = mapped_column(nullable=True)
    weekday_id: Mapped[str] = mapped_column()

    UniqueConstraint("weekday", "time", "practice", "num", "name", "teacher", name='uix_1')

    def __repr__(self):
        return f"{self.weekday}, {self.time}, {self.practice}, {self.num}, {self.name}, {self.teacher}, {self.groups}, {self.room}, {self.other}"


def init_database():
    """ Инициализация моделей """
    # schedule_db.create_tables(BaseModel.__subclasses__())
    Base.metadata.create_all(bind=engine)
