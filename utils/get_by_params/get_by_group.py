from database.init_database import Schedule
from utils.misc.write_to_csv import write_to_csv


def get_by_group(group_number: str) -> None:
    """ Получение расписания занятий группы. """
    results = Schedule.select().where(
        Schedule.groups == group_number
    ).order_by(Schedule.weekday_id, Schedule.time)
    for i_class in results:
        print(i_class)
    write_to_csv(param_name="group_number", param_value=group_number, data=results.tuples())
