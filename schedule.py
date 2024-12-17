print("silly")
import pandas as pd
import numpy as np
import matplotlib as mpl
import random

# Initialize arrays for each day of the week
monday = np.full(28, "----------")
tuesday = np.full(28, "----------")
wednesday = np.full(28, "----------")
thursday = np.full(28, "----------")
friday = np.full(28, "----------")

# Classes and their times
# Time format is in days of week [space] start time without colons [space] end time without colons (both 24 hr time)
# Thursday is H because I couldn't figure out how to separate by capitalized letter
classes = {
    "ANTH 0800": "MWF 1300 1400",
    "COLT 1710C": "M 1500 1730",
    #"CSCI 1430": "TH 900 1030",
    #"ECON 1390": "TH 900 1030",
    "ECON 1629": "TH 1300 1430",
    "ECON 1820": "MW 830 1000",
    "LING 1615": "MWF 1200 1300",
    "LING 1741": "W 1500 1730",
    "PHIL 1485": "MWF 1200 1300",
    "POLS 1140": "MWF 1400 1500"
}

# Labs/sections that have same keys as corresponding class in classes
labs = {
    "ECON 1629": "M 1800 1900"
}

class_keys = list(classes.keys())
picked_classes = {}

# Add classes that are already picked
picked_classes["MUSC 0610"] = "TH 1900 2200"
picked_classes["MUSC 0550"] = "TH 1430 1600"
picked_classes["CSCI 1230"] = "TH 1030 1200"
picked_classes["MUSC 1120"] = "W 930 1200"

# Function to find overlaps between times
def find_overlap(class_name):
    split_times = classes[class_name].split()
    # second member of string
    start = int(split_times[1])
    # third member of string
    end = int(split_times[2])
    all_days = list(split_times[0])
    picked_keys = list(picked_classes.keys())

    # all classes that are already picked
    for picked_class in picked_keys:
        picked_split_times = picked_classes[picked_class].split()
        day_overlap = any(day in picked_split_times[0] for day in all_days)
        if day_overlap:
            picked_start = int(picked_split_times[1])
            picked_end = int(picked_split_times[2])
            # Find time overlap
            if (picked_start < start < picked_end) or (picked_start < end < picked_end) or \
               (start < picked_start < end) or (start < picked_end < end):
                return True
        # if current class has a lab
        if class_name in labs:
            split_times = labs[class_name].split()
            lab_start = int(split_times[1])
            lab_end = int(split_times[2])
            all_days = list(split_times[0])
            day_overlap = any(day in picked_split_times[0] for day in all_days)
            if day_overlap:
                picked_start = int(picked_split_times[1])
                picked_end = int(picked_split_times[2])
                # Find time overlap
                if (picked_start < lab_start < picked_end) or (picked_start < lab_end < picked_end) or \
                (lab_start < picked_start < lab_end) or (lab_start < picked_end < lab_end):
                    return True
    return False

# Pick random classes
for _ in range(2):
    attempts = 0
    max_attempts = 1000
    while attempts < max_attempts:
        rand_key = class_keys[random.randrange(len(class_keys))]
        # conditions to add random class to schedule
        if rand_key not in picked_classes and not find_overlap(rand_key):
            picked_classes[rand_key] = classes[rand_key]
            # adds labs to picked classes
            if rand_key in labs:
                rand_key_lab = rand_key + "L"
                picked_classes[rand_key_lab] = labs[rand_key]
            class_keys.remove(rand_key)
            print(rand_key)
            break
        attempts += 1
    if attempts == max_attempts:
        print("Could not find non-overlapping class within the attempt limit.")
        break

# Function to convert time string to array index
def time_to_index(time_str):
    time = int(time_str)
    index = (time // 100 - 8) * 2
    if time % 100 == 30:
        index += 1
    return index

# Function to convert string to corresponding array
def find_array(day):
    array = []
    if day == "M":
        array = monday
    elif day == "T":
        array = tuesday
    elif day == "W":
        array = wednesday
    elif day == "H":
        array = thursday
    elif day == "F":
        array = friday
    return array

# Function to add classes to schedule
def find_and_add_times(picked_class, start, end, day_array):
    start_index = time_to_index(start)
    end_index = time_to_index(end)
    for i in range(start_index, end_index):
        day_array[i] = picked_class

# Add classes to schedule
for key in picked_classes:
    split_str = picked_classes[key].split()
    days = list(split_str[0])
    for day in days:
        find_and_add_times(key, split_str[1], split_str[2], find_array(day))

# Create and display DataFrame
df = pd.DataFrame({
    "Monday": monday,
    "Tuesday": tuesday,
    "Wednesday": wednesday,
    "Thursday": thursday,
    "Friday": friday
})

# Add time labels
time_labels = ["8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM",
               "12:30 PM", "1:00 PM", "1:30 PM", "2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM",
               "5:00 PM", "5:30 PM", "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM", "9:00 PM",
               "9:30 PM"]

df.index = time_labels

df.style \
  .format(precision=3, thousands=".", decimal=",") \
  .format_index(str.upper, axis=1)