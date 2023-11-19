Sites - folder contains actual txt files with HTML code of schedule sites.
Sites1 - folder contains previous txt files with HTML code of schedule sites.
main.py - python script that creates and outputs a schedule.

    DELETE_FILES - delete all files in Site folder. Set the value to "True" if you want to completely update the schedule, "False" if outdated files are deleted.
    UPDATE_TXT - checking of the existence of txt files and downloading them in case of absence. Set the value to "True" if the schedule from the site is not fully loaded, "False" if the schedule from the site is fully loaded.
    UPDATE_JSON - is need to update json file. Set the value to "False" if the schedule from the site is fully loaded and the json file is updated (the schedule is read from this file), "False" if the schedule from the site is not loaded or not fully loaded.

    PROPERTY_TO_FILD - the name of the field to search for.
    PROPERTY_VALUE - the field value you are looking for.
    DEPARTMENTS_TO_FIND - the list of departments for which the schedule will be downloaded from the sites.

room_8_k_322.json - the json file contains a schedule with the specified field value.
schedule.json - the json file contains the full schedule of the specified departments.
schedule.xlsx - xlsx file containing room_8_k_322.json data in xlsx format.
