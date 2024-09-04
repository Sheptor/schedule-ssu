from database.init_database import Schedule, session
import utils


def get_by_teacher(teacher_name: str) -> None:
    """ Получение расписания занятий преподавателя. """
    results = session.query(Schedule).where(
        Schedule.teacher.like(f"%{teacher_name}%")
    ).order_by(Schedule.weekday_id, Schedule.time).all()
    utils.schedule_result =  results
