from database.init_database import Schedule, session
import utils


def get_by_group(group_number: str) -> None:
    """ Получение расписания занятий группы. """
    results = session.query(Schedule).where(
        Schedule.groups.like(f"%{group_number}%")
    ).order_by(Schedule.weekday_id, Schedule.time).all()
    utils.schedule_result =  results