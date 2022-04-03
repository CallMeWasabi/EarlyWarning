import json
from operator import index
import random
from matplotlib.font_manager import json_dump

from scipy import rand

filename = "Simulate_dataJSON_v1.json"
hour, minute, secode = 0, 0, -1 

def getTime(hour, minute, second):
    if (hour == 0 and minute == 0 and second == -1):
        return hour, minute, second + 1
    elif (second + 10 == 60):
        second = 0
        minute += 1
        if (minute == 60):
            hour += 1
            minute = 0
    elif (second + 10 != 60):
        second += 10
    return hour, minute, second
    
def write_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def generate_json_v1(filename):
    list_parent = []
    hour, minute, second = 0, 0, -1
    for i in range(8640):
        dict_child = {}
        hour, minute, second = getTime(hour, minute, second)
        dict_child["id"] = i
        if (hour < 10 and minute < 10 and second < 10):
            dict_child["date_time"] = "0{}:0{}:0{}".format(hour, minute, second)
        elif (hour < 10 and minute > 9 and second > 9):
            dict_child["date_time"] = "0{}:{}:{}".format(hour, minute, second)
        elif (hour > 9 and minute < 10 and second > 9):
            dict_child["date_time"] = "{}:0{}:{}".format(hour, minute, second)
        elif (hour > 9 and minute > 9 and second < 10):
            dict_child["date_time"] = "{}:{}:0{}".format(hour, minute, second)
        elif (hour < 10 and minute < 10 and second > 9):
            dict_child["date_time"] = "0{}:0{}:{}".format(hour, minute, second)
        elif (hour < 10 and minute > 9 and second < 10):
            dict_child["date_time"] = "0{}:{}:0{}".format(hour, minute, second)
        elif (hour > 9 and minute < 10 and second < 10):
            dict_child["date_time"] = "{}:0{}:0{}".format(hour, minute, second)
        else : dict_child["date_time"] = "{}:{}:{}".format(hour, minute, second)
        dict_child["quantity_rain"] = str(random.randint(-20, 140))
        dict_child["quantity_water"] = str(random.randint(10, 50))
        dict_child["temperature"] = str(random.randint(15, 40))
        dict_child["humidity"] = str(random.randint(20, 80))
        dict_child["hardware_fail"] = str(random.randint(0,1))
        list_parent.append(dict_child)
    write_json(list_parent, filename)

def generate_json_v2(filename):
    dict_parent = {}
    hour, minute, second = 0, 0, -1
    list_id = []
    list_date_time = []
    list_quantity_rain = []
    list_quantity_water = []
    list_temperature = []
    list_humidity = []
    for i in range(8640):
        hour, minute, second = getTime(hour, minute, second)
        list_id.append(i)
        if (hour < 10 and minute < 10 and second < 10):
            list_date_time.append("0{}:0{}:0{}".format(hour, minute, second))
        elif (hour < 10 and minute > 9 and second > 9):
            list_date_time.append("0{}:{}:{}".format(hour, minute, second))
        elif (hour > 9 and minute < 10 and second > 9):
            list_date_time.append("{}:0{}:{}".format(hour, minute, second))
        elif (hour > 9 and minute > 9 and second < 10):
            list_date_time.append("{}:{}:0{}".format(hour, minute, second))
        elif (hour < 10 and minute < 10 and second > 9):
            list_date_time.append("0{}:0{}:{}".format(hour, minute, second))
        elif (hour < 10 and minute > 9 and second < 10):
            list_date_time.append("0{}:{}:0{}".format(hour, minute, second))
        elif (hour > 9 and minute < 10 and second < 10):
            list_date_time.append("{}:0{}:0{}".format(hour, minute, second))
        else : list_date_time.append("{}:{}:{}".format(hour, minute, second))
        
        list_quantity_rain.append(str(random.randint(-20, 140)))
        list_quantity_water.append(str(random.randint(10, 50)))
        list_temperature.append(str(random.randint(15, 40)))
        list_humidity.append(str(random.randint(20, 80)))
    dict_parent["id"] = list_id
    dict_parent["date_time"] = list_date_time
    dict_parent["quantity_rain"] = list_quantity_rain
    dict_parent["quantity_water"] = list_quantity_water
    dict_parent["temperature"] = list_temperature
    dict_parent["humidity"] = list_humidity
    write_json(dict_parent, filename)

generate_json_v1(filename=filename)