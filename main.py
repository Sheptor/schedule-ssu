import re
import requests
import os
import time
import random
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


def get_timer(seconds_count: int) -> Tuple:
    """ The function recalculates the number of seconds to the h:m:s format """
    l_h = seconds_count // 3600
    l_m = (seconds_count - l_h * 3600) // 60
    l_s = seconds_count - (l_h * 3600 + l_m * 60)
    return l_h, l_m, l_s


def get_department_list(url: str) -> Dict:
    """
    The function gets links to the schedule of institutes and faculties
    from the website and returns the dictionary {institute: link to schedule}

    Arguments:
        url (str): SSU schedule homepage website URL

    :return: department_link_dict
    :rtype: Dict[str, str]
    """
    home_site_file_name = os.path.join(DIRECTORY, "Sites", "Home.txt")

    if UPDATE_TXT:
        with open(home_site_file_name, "w",
                  encoding="utf-8") as home_file:

            site_text = requests.get(url).text
            pattern = r"<h2>Группы(.+?)</ul></div>"
            site_text = re.search(pattern, site_text)[0]
            if site_text is not None:
                home_file.write(site_text)

        time.sleep(REQUEST_TIME)

    with open(home_site_file_name, "r",
              encoding="utf-8") as home_file:
        site_text = home_file.read()
        pattern = r"<li><a href='(.+?)'>(.+?)</a></li>"
        links_list = re.findall(pattern, site_text)

        department_link_dict = {k_department: i_link for i_link, k_department in links_list
                                if k_department in DEPARTMENTS_TO_FIND}

        return department_link_dict


def get_groups(url, department_name: str) -> Dict:
    """
    The function from the site provides a link to the schedule of classes
    of the institute group and returns a dictionary containing information
    about the link to the schedule of the group, the name of the file in
    which the information from the site is stored (None), the schedule
    of activities (None)

    Arguments:
        url (str): group schedule website URL
        department_name (str): name of the institute

    :return: groups_dict
    :rtype: Dict[str, Dict[str, Optional[str]]]
    """
    department_site_file_name = os.path.join(DIRECTORY, "Sites", f"{department_name}.txt")

    if UPDATE_TXT:
        with open(department_site_file_name, "w",
                  encoding="utf-8") as department_file:
            site_text = requests.get(url).text
            department_file.write(site_text)
        time.sleep(REQUEST_TIME)

    with open(department_site_file_name, "r",
              encoding="utf-8") as department_file:
        site_text = department_file.read()
        pattern = r'<a href="(.+?)">(\d{3,4})</a>'
        groups_list = re.findall(pattern, site_text)

        groups_dict = {i_group: {"link": i_link, "file": None, "schedule": None} for i_link, i_group in groups_list}

        return groups_dict


def get_group_schedule(
        url: str, department_name: str,
        group_number: str,
        current_group_index: int,
        group_in_department_index: int) -> None:
    """
    The function adds the name of the group schedule file
    and the group schedule to the schedule dictionary

    Arguments:
        url (str): group schedule website URL
        department_name (str): name of the institute
        group_number (str): group number
        current_group_index (int): index of the group in the entire list
        group_in_department_index (int): index of the group in the institute list

    :return: None
    """
    global total_time
    group_site_file_name = os.path.join(DIRECTORY, "Sites", f"{department_name}_{group_number}.txt")

    if UPDATE_TXT:
        if not os.path.exists(group_site_file_name):
            site_text = requests.get(url).text
            res = re.search(r"</colgroup>(.+)</span>", site_text)
            if res is not None:
                with open(group_site_file_name, "w",
                          encoding="utf-8") as group_file:
                    group_file.write(res[0])
                    hours, minutes, seconds = get_timer(total_time)
                print(f"saved {department_name} {group_number}"
                      f"\t\t\t{group_in_department_index}/{len(schedule[department_name]['groups'])} "
                      f"({round((group_in_department_index/len(schedule[department_name]['groups']) * 100), 2)}%)"
                      f"\t\t\t{current_group_index}/{total_groups} "
                      f"({round((current_group_index/total_groups) * 100, 2)}%)"
                      f"\t\t\ttime left: {hours}h:{minutes}m:{seconds}s")
            time.sleep(REQUEST_TIME)

    total_time -= 50
    if os.path.exists(group_site_file_name):

        schedule[i_department]["groups"][group_number]["file"] = group_site_file_name
        schedule[i_department]["groups"][group_number]["schedule"] = make_schedule(
            schedule_file_name=group_site_file_name
        )


def make_schedule(schedule_file_name: str) -> Dict[str, List[Dict[str, str]]]:
    """
    The function gets the schedule of the group
    from the file and returns it as a dictionary

    Arguments:
        schedule_file_name: schedule file name

    :return: group schedule
    :rtype: Dict[str, List[Dict[str, str]]]
    """

    def is_none(var, index=1):
        if var is not None:
            return var[index]
        else:
            return "---"

    group_schedule = dict()

    with open(schedule_file_name, "r", encoding="utf-8") as schedule_file:
        lesson_to_time = {
            1: "08:20-09:50",
            2: "10:00-11:35",
            3: "12:05-13:40",
            4: "13:50-15:25",
            5: "15:35-17:10",
            6: "17:20-18:40",
            7: "18:45-20:05",
            8: "20:10-21:30",
        }
        file_text = schedule_file.read()
        for i_day_index, i_day in enumerate(("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"),
                                            start=1):
            pattern = r"<td  id='\d_" + str(i_day_index) + "' class=''>(.*?)</td>"
            day_list = re.findall(pattern, file_text)
            group_schedule[i_day] = []
            for j_lesson_index, j_lesson in enumerate(day_list, start=1):
                sub_lessons = re.findall(
                    r"<div class='l l--t-\d l--r-\d l--g-\d'>(.+?</div></div>.+?)</div></div>", j_lesson)

                if not len(sub_lessons):
                    group_schedule[i_day].append([{
                        "Time": "---",
                        "Even": "---",
                        "Type": "---",
                        "Name": "---",
                        "Teacher": "---",
                        "Room": "---"
                    }])

                for k_sub_lesson in sub_lessons:
                    group_schedule[i_day].append([])
                    lesson_time = lesson_to_time[j_lesson_index]
                    even = is_none(re.search(r"alt='Чётность'>(.*?)</div>", k_sub_lesson))
                    lesson_type = is_none(re.search(r"alt='Тип'>(.*?)</div>", k_sub_lesson))
                    lesson_name = is_none(re.search(r"<div class='l-dn'>(.*?)</div>", k_sub_lesson))
                    teacher = is_none(re.search(r"<div class='l-tn'>(<a href.+?>)?(.*?)(</a>)?</div>", k_sub_lesson),
                                      index=2)
                    room = is_none(re.search(r"<div class='l-p'>(.*?)$", k_sub_lesson))
                    group_schedule[i_day][j_lesson_index-1].append({
                        "Time": lesson_time,
                        "Even": even,
                        "Type": lesson_type,
                        "Name": lesson_name,
                        "Teacher": teacher,
                        "Room": room
                    })

    return group_schedule


if __name__ == '__main__':
    # Define global variables ##########################################################################################
    DELETE_FILES: bool = False  # Delete all files in Site folder
    UPDATE_TXT: bool = False  # Checking of the existence of txt files and downloading them in case of absence
    UPDATE_JSON: bool = True  # Is need to update json file

    REQUEST_TIME = random.randint(40, 50) + random.random()  # Time between requests

    PROPERTY_TO_FIND: str = "Room"  # "Room" # Acceptable values: "Room", "Teacher", "Name"
    PROPERTY_VALUE: str = r"8 корп. ауд. 322".lower()  # "8 корп. ауд. 322"
    DEPARTMENTS_TO_FIND: Tuple = ("Институт физики",)  # ("Биологический факультет", "Географический факультет",
    # "Геологический факультет", "Институт дополнительного профессионального образования", "Институт искусств",
    # "Институт истории и международных отношений", "Институт физики", "Институт физической культуры и спорта",
    # "Институт филологии и журналистики", "Институт химии", "Механико-математический факультет",
    # "Социологический факультет", "Факультет иностранных языков и лингводидактики",
    # "Факультет компьютерных наук и информационных технологий", "Факультет психологии",
    # "Факультет психолого-педагогического и специального образования",
    # "Факультет фундаментальной медицины и медицинских технологий",
    # "Философский факультет", "Экономический факультет", "Юридический факультет", "Геологический колледж",
    # "Колледж радиоэлектроники им. П.Н. Яблочкова", "Психолого-педагогический факультет",
    # "Факультет математики и естественных наук", "Филологический факультет")

    DIRECTORY: str = os.getcwd()  # Get current working directory

    schedule = dict()
    total_groups = 0
    if not os.path.exists(os.path.join(DIRECTORY, 'Sites')):
        os.mkdir(os.path.join(DIRECTORY, 'Sites'))

    # Delete files from Sites folder ###################################################################################
    if DELETE_FILES:
        confirm = input(f"Вы действительно хотите удалить все файлы из директории "
                        f"{os.path.join(DIRECTORY, 'Sites')} ?\n[y/n] >>> ").lower()
        if confirm == "y":
            for i_file in os.listdir(os.path.join(DIRECTORY, "Sites")):
                os.remove(os.path.join(DIRECTORY, "Sites", i_file))

    # Update schedule ##################################################################################################
    if UPDATE_JSON:
        department_links = get_department_list("https://www.sgu.ru/schedule")
        for i_department in department_links:
            schedule[i_department] = {"Schedule link": department_links[i_department]}

        # Get text from https://sgu.ru #################################################################################
        for i_department in schedule:
            groups = get_groups("https://sgu.ru" + schedule[i_department]["Schedule link"], i_department)
            schedule[i_department]["groups"] = groups
            total_groups += len(groups)

        department_count = len(schedule)
        group_index = 0
        total_time = total_groups * 50

        # Get text from groups #########################################################################################
        for i_department in schedule:
            # print(f"\n{i_department}:")

            for j_group_index, j_group in enumerate(schedule[i_department]["groups"], start=1):
                group_index += 1
                get_group_schedule(
                    url="https://sgu.ru" + schedule[i_department]["groups"][j_group]["link"],
                    department_name=i_department,
                    group_number=j_group,
                    current_group_index=group_index,
                    group_in_department_index=j_group_index
                )

        # Save results to schedule.json ################################################################################
        with open("schedule.json", "w", encoding="ascii") as json_file:
            json.dump(schedule, json_file, indent=4)

    # Get results from schedule.json ###################################################################################
    with open('schedule.json') as json_file:
        schedule = json.load(json_file)

    # Save room schedule to json file ##################################################################################
    room_schedule = get_room(PROPERTY_TO_FIND, PROPERTY_VALUE)
    with open("sought_schedule.json", "w", encoding="ascii") as json_file:
        json.dump(room_schedule, json_file, indent=4)

    # Test 1 ###########################################################################################################
    print("Test 1:")
    for i_lesson in room_schedule:
        print(i_lesson)

    # Save room schedule to xlsx file ##################################################################################
    days_list = [i_lesson["Day"] for i_lesson in room_schedule]
    time_list = [i_lesson["Time"] for i_lesson in room_schedule]
    departments_list = [i_lesson["Department"] for i_lesson in room_schedule]
    groups_in_room_list = [i_lesson["Group"] for i_lesson in room_schedule]
    evens_list = [i_lesson["Even"] for i_lesson in room_schedule]
    types_list = [i_lesson["Type"] for i_lesson in room_schedule]
    names_list = [i_lesson["Name"] for i_lesson in room_schedule]
    teachers_list = [i_lesson["Teacher"] for i_lesson in room_schedule]
    rooms_list = [i_lesson["Room"] for i_lesson in room_schedule]

    # Test 2 ###########################################################################################################
    # print("\nTest 2")
    # print(schedule["Институт физики"]["groups"]["1051"]["schedule"])
    # print(schedule["Институт физики"]["groups"]["1252"]["schedule"])

    data = pd.DataFrame({
        "День недели": days_list,
        "Время": time_list,
        "Институт/факультет": departments_list,
        "Группа": groups_in_room_list,
        "Четность": evens_list,
        "Тип (пр. лаб. лек.)": types_list,
        "Название предмета": names_list,
        "Преподаватель": teachers_list,
        "Аудитория": rooms_list
    })
    data.to_excel("Schedule.xlsx", sheet_name=PROPERTY_VALUE, index=False)

    print()
    print("=" * 40)
    print("The End!")
    print("=" * 40)
