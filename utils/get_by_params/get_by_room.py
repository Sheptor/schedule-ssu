from database.init_database import Schedule
from utils.misc.write_to_csv import write_to_csv


def get_by_room(room: str) -> None:
    """ Получение расписания занятий аудитории. """
    results = Schedule.select().where(
        Schedule.room.contains(f"{room}")
    ).order_by(Schedule.weekday_id, Schedule.time)
    for i_class in results:
        print(i_class)
    write_to_csv(param_name="room", param_value=room, data=results.tuples())
