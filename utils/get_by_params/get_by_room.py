from database.init_database import Schedule, session
import utils


def get_by_room(building: str, room: str) -> None:
    """ Получение расписания занятий аудитории. """
    results = session.query(Schedule).where(
        Schedule.room.like(f"%{building}%{room}%")
    ).order_by(Schedule.weekday_id, Schedule.time).all()
    utils.schedule_result =  results
