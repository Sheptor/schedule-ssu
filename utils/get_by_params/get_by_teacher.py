from database.init_database import Schedule
from utils.misc.write_to_csv import write_to_csv


def get_by_teacher(teacher_name: str) -> None:
    """ Получение расписания занятий преподавателя. """
    results = Schedule.select().where(
        Schedule.teacher == teacher_name
    ).order_by(Schedule.weekday_id, Schedule.time)
    for i_class in results:
        print(i_class)
    write_to_csv(param_name="teacher_name", param_value=teacher_name, data=results.tuples())
