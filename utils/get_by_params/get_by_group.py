from database.init_database import Schedule
import utils


def get_by_group(group_number: str) -> None:
    """ Получение расписания занятий группы. """
    results = Schedule.select().where(
        Schedule.groups.contains(group_number)
    ).order_by(Schedule.weekday_id, Schedule.time)
    utils.schedule_result =  results