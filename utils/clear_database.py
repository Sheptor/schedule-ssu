from database.init_database import init_database, Schedule, Department, Group, Weekdays


def clear_database():
    """ Удаление всех данных из базы данных. """
    confirm = input(f"Вы действительно хотите очистить базу данных?\n[y/n] >>> ").lower()
    if confirm == "y":
        Group.drop_table()
        Department.drop_table()
        Schedule.drop_table()
        Weekdays.drop_table()
        init_database()
