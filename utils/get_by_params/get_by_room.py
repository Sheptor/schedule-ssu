from database.init_database import Schedule
import utils


def get_by_room(building: str, room: str) -> None:
    """ Получение расписания занятий аудитории. """
    results = Schedule.select().where(
        Schedule.room ** f"%{building}%{room}%"
    ).order_by(Schedule.weekday_id, Schedule.time)
    utils.schedule_result =  results
