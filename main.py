from database.init_database import init_database, Schedule, Department, Group
from utils.get_status import get_status
from utils.wait import wait
from utils.update_schedule import update_schedule
from utils.misc.get_updateable_departments import get_updatable_departments
import re
import requests
import os
import json
import pandas as pd
from typing import Dict, Tuple, List


def get_room(property_name: str, property_value: str) -> List:
    """
    The function returns the class schedule for the room

    Arguments:
        key:
        room (str): Number of the room

    :return: res_list
    :rtype: List[Dict]
    """
    def day_to_num(day: str) -> int:
        days_dict = {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6,
            "Sunday": 7
        }
        return days_dict.get(day)

    res_list = []
    for local_i_department in schedule:
        for local_j_group in schedule[local_i_department]["groups"]:
            if schedule[local_i_department]["groups"][local_j_group]["schedule"] is not None:
                for k_group_schedule_day in schedule[local_i_department]["groups"][local_j_group]["schedule"]:
                    for l_lesson \
                            in schedule[local_i_department]["groups"][local_j_group]["schedule"][k_group_schedule_day]:
                        for m_sub_lesson in l_lesson:
                            # if m_sub_lesson[property_name] == property_value:
                            if re.search(property_value, m_sub_lesson[property_name].lower()):
                                res_list.append({
                                    "Day": k_group_schedule_day,
                                    "Time": m_sub_lesson["Time"],
                                    "Department": local_i_department,
                                    "Group": local_j_group,
                                    "Even": m_sub_lesson["Even"],
                                    "Type": m_sub_lesson["Type"],
                                    "Name": m_sub_lesson["Name"],
                                    "Teacher": m_sub_lesson["Teacher"],
                                    "Room": m_sub_lesson["Room"]
                                })

    return sorted(res_list, key=lambda x: (day_to_num(x["Day"]), x["Time"]))


if __name__ == '__main__':
    # Define global variables ##########################################################################################
    # DELETE_FILES: bool = False  # Delete all files in Site folder
    # UPDATE_TXT: bool = False  # Checking of the existence of txt files and downloading them in case of absence
    # UPDATE_JSON: bool = False  # Is need to update json file

    CLEAR_DATABASE: bool = False
    UPDATE_LINKS: bool = False
    UPDATE_DATABASE = True

    departments_to_update = ("Институт физики",)  # Update only Институт физики
    # departments_to_update = None  # Update all
    departments_to_update = get_updatable_departments(departments_to_update)
    init_database()

    # Delete files from Sites folder ###################################################################################
    if CLEAR_DATABASE:
        confirm = input(f"Вы действительно хотите очистить базу данных?\n[y/n] >>> ").lower()
        if confirm == "y":
            Group.drop_table()
            Department.drop_table()
            Schedule.drop_table()
            init_database()

    # Update schedule ##################################################################################################
    if UPDATE_DATABASE:
        update_schedule(update_links=UPDATE_LINKS, departments_to_update=departments_to_update)

    # # Get results from schedule.json ###################################################################################
    # with open('schedule.json') as json_file:
    #     schedule = json.load(json_file)
    #
    # # Save room schedule to json file ##################################################################################
    # room_schedule = get_room(PROPERTY_TO_FIND, PROPERTY_VALUE)
    # with open("sought_schedule.json", "w", encoding="ascii") as json_file:
    #     json.dump(room_schedule, json_file, indent=4)
    #
    # # Test 1 ###########################################################################################################
    # print("Test 1:")
    # for i_lesson in room_schedule:
    #     print(i_lesson)
    #
    # # Save room schedule to xlsx file ##################################################################################
    # days_list = [i_lesson["Day"] for i_lesson in room_schedule]
    # time_list = [i_lesson["Time"] for i_lesson in room_schedule]
    # departments_list = [i_lesson["Department"] for i_lesson in room_schedule]
    # groups_in_room_list = [i_lesson["Group"] for i_lesson in room_schedule]
    # evens_list = [i_lesson["Even"] for i_lesson in room_schedule]
    # types_list = [i_lesson["Type"] for i_lesson in room_schedule]
    # names_list = [i_lesson["Name"] for i_lesson in room_schedule]
    # teachers_list = [i_lesson["Teacher"] for i_lesson in room_schedule]
    # rooms_list = [i_lesson["Room"] for i_lesson in room_schedule]
    #
    # # Test 2 ###########################################################################################################
    # # print("\nTest 2")
    # # print(schedule["Институт физики"]["groups"]["1051"]["schedule"])
    # # print(schedule["Институт физики"]["groups"]["1252"]["schedule"])
    #
    # data = pd.DataFrame({
    #     "День недели": days_list,
    #     "Время": time_list,
    #     "Институт/факультет": departments_list,
    #     "Группа": groups_in_room_list,
    #     "Четность": evens_list,
    #     "Тип (пр. лаб. лек.)": types_list,
    #     "Название предмета": names_list,
    #     "Преподаватель": teachers_list,
    #     "Аудитория": rooms_list
    # })
    # data.to_excel("Schedule.xlsx", sheet_name=PROPERTY_VALUE, index=False)

    print()
    print("=" * 40)
    print("The End!")
    print("=" * 40)
