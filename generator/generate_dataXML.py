import xml.etree.ElementTree as et
import random
import datetime

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

def generateXML(filename):
    root = et.Element("Infomation")
    hour, minute, second, id = 0, 0, -1, 0
    for i in range(8640):
        dt = et.Element("data")
        hour, minute, second = getTime(hour, minute, second)
        t = datetime.datetime.now()
        root.append(dt)
        dt.set("id", str(id))
        id += 1
        if (hour < 10 and minute < 10 and second < 10):
            dt.set("date_time", "0{}:0{}:0{}".format(hour, minute, second))
        elif (hour < 10 and minute > 9 and second > 9):
            dt.set("date_time", "0{}:{}:{}".format(hour, minute, second))
        elif (hour > 9 and minute < 10 and second > 9):
            dt.set("date_time", "{}:0{}:{}".format(hour, minute, second))
        elif (hour > 9 and minute > 9 and second < 10):
            dt.set("date_time", "{}:{}:0{}".format(hour, minute, second))
        elif (hour < 10 and minute < 10 and second > 9):
            dt.set("date_time", "0{}:0{}:{}".format(hour, minute, second))
        elif (hour < 10 and minute > 9 and second < 10):
            dt.set("date_time", "0{}:{}:0{}".format(hour, minute, second))
        elif (hour > 9 and minute < 10 and second < 10):
            dt.set("date_time", "{}:0{}:0{}".format(hour, minute, second))
        else : dt.set("date_time", "{}:{}:{}".format(hour, minute, second))
        
        dt.set("quantity_rain", str(random.randint(-20, 140))) # 0 - 100 default
        dt.set("quantity_water", str(random.randint(10, 50))) # 20 - 40
        dt.set("temperature", str(random.randint(15, 40)))
        dt.set("humidity", str(random.randint(20, 80))) # 20 - 35
        if i == 7 or i == 567 or i == 2344 or i == 7643:
            dt.set("hardware_fail", str(1))
        else: dt.set("hardware_fail", str(0))

    tree = et.ElementTree(root)
    with open(filename, "wb") as files:
        tree.write(files)

generateXML("test1.xml")