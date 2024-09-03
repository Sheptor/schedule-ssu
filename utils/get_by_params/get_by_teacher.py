from database.init_database import Schedule
import utils


def get_by_teacher(teacher_name: str) -> None:
    """ Получение расписания занятий преподавателя. """
    results = Schedule.select().where(
        Schedule.teacher.contains(teacher_name)
    ).order_by(Schedule.weekday_id, Schedule.time)
    utils.schedule_result =  results
