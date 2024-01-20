from database.init_database import Schedule, Weekdays
from utils.misc.write_to_csv import write_to_csv


def get_by_teacher(teacher_name: str, is_write_to_csv: bool) -> None:
    """ Получение расписания занятий преподавателя. """
    results = Schedule.select().join(Weekdays, on=(
            Schedule.day == Weekdays.day_name)
                                     ).where(Schedule.teacher_name == teacher_name).order_by(Weekdays.id)
    for i_class in results:
        print(i_class)
    if is_write_to_csv:
        write_to_csv(param_name="teacher_name", param_value=teacher_name, data=results.tuples())
