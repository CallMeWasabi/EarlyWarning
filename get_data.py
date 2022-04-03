import xml.etree.ElementTree as et
from itsdangerous import json
import pandas as pd
from tkinter import *
from constant import *
import json 
import sys
import os



class Provider:
    
    def __init__(self, frame_setting="", master="", list_key=["date_time", "quantity_rain", "quantity_water", "temperature", "humidity"]) -> None:
        self.frame_setting = frame_setting
        self.master = master

        # variable
        self.typefile = ""
        self.dict_limit = {
            "min_quantity_rain" : 0,
            "max_quantity_rain" : 0,
            "min_quantity_water" : 0,
            "max_quantity_water" : 0,
            "min_temperature" : 0,
            "max_temperature" : 0,
            "min_humidity" : 0,
            "max_humidity" : 0,
        }
    
        self.id = 0
        self.id_in_insert = 1
        self.child_id = 0
        self.index_id = 0
        self.tree_id = 1
        self.iid = 0
        self.graph_id = 0
        self.station_id = 0
        self.df = None
        self.list_keys = list_key
        
        self.load_config()
        print(self.typefile)
        if self.typefile == ".xml\n":
            self.df = self.get_dataframe_xml()
        elif self.typefile == ".json\n":
            self.df = self.get_dataframe_json()
        else:
            self.df = self.get_dataframe_xml()
             
        # ["date_time", "quantity_rain", "quantity_water", "temperature", "humidity"]
        
        # Variable in Entry and Radio
        self.TypeFile_var = IntVar()
        self.min_quantity_rain_var = StringVar()
        self.max_quantity_rain_var = StringVar()
        self.min_quantity_water_var =StringVar()
        self.max_quantity_water_var =StringVar()
        self.min_temperature_var = StringVar()
        self.max_temperature_var = StringVar()
        self.min_humidity_var = StringVar()
        self.max_humidity_var = StringVar()
        
    def load_config(self):
        try:
            with open("config.txt", "r") as f:
                for line in f:
                    (key, value) = line.split("=")
                    if key == "type_file":
                        self.typefile = value
                    else:
                        self.dict_limit[key] = int(value)
                f.close()
            self.update_dict()          
        except FileNotFoundError:
            self.set_default()
    
    
    def update_dict(self):
        with open("config.txt", "r") as f:
            for line in f:
                (key, value) = line.split("=")
                if key == "type_file":
                    self.typefile = value
                else:
                    self.dict_limit[key] = int(value)
    
    
    def update_config(self):        
        with open("config.txt", "w") as f:
            list_data = []
            list_data.append(f"type_file={self.typefile}\n")
            for i in range(1,5):
                list_data.append(f"min_{self.list_keys[i]}=" + str(self.dict_limit[f"min_{self.list_keys[i]}"]) + "\n")
                list_data.append(f"max_{self.list_keys[i]}=" + str(self.dict_limit[f"max_{self.list_keys[i]}"]) + "\n")
            f.writelines(list_data)
            f.close()
        self.update_dict()
    
    
    def set_default(self):
        
        # default setting
        self.typefile = ".xml"
        self.dict_limit["min_quantity_rain"] = 0
        self.dict_limit["max_quantity_rain"] = 100
        self.dict_limit["min_quantity_water"] = 20
        self.dict_limit["max_quantity_water"] = 40
        self.dict_limit["min_temperature"] = 20
        self.dict_limit["max_temperature"] = 35
        self.dict_limit["min_humidity"] = 20
        self.dict_limit["max_humidity"] = 60
        self.update_config()
    
    
    def set_value(self):
        
        def checktype(_list):
            for i in range(8):
                if not _list[i].isnumeric():
                    return False
            return True
        
        # get value from entry
        _typefile_id = self.TypeFile_var.get()
        _min_quantity_rain_var = self.min_quantity_rain_var.get()
        _max_quantity_rain_var = self.max_quantity_rain_var.get()
        _min_quantity_water_var = self.min_quantity_water_var.get()
        _max_quantity_water_var = self.max_quantity_water_var.get()
        _min_temperature_var = self.min_temperature_var.get()
        _max_temperature_var = self.max_temperature_var.get()
        _min_humidity_var = self.min_humidity_var.get()
        _max_humidity_var = self.max_humidity_var.get() 

        # append data
        _list = []
        _list.append(_min_quantity_rain_var)
        _list.append(_max_quantity_rain_var)
        _list.append(_min_quantity_water_var)
        _list.append(_max_quantity_water_var)
        _list.append(_min_temperature_var)
        _list.append(_max_temperature_var)
        _list.append(_min_humidity_var)
        _list.append(_max_humidity_var)
        
        
        if _typefile_id == 1:
            self.typefile = ".json"
        elif _typefile_id == 0:
            self.typefile = ".xml"
        
        if checktype(_list):
            index_list = 0
            for i in range(1, 5):
                self.dict_limit[f"min_{self.df.keys()[i]}"] = _list[index_list]
                self.dict_limit[f"max_{self.df.keys()[i]}"] = _list[index_list+1]
                index_list += 2
            self.update_config()
            
            label_apply = Label(self.frame_setting, text="Apply Completed", font=get_font(14), fg="green")
            label_apply.place(x=150, y=300)
            label_restart = Label(self.frame_setting, text="Need to restart app", font=get_font(14), fg="#cc3300")
            label_restart.place(x=330, y=300)
            label_apply.after(2000, lambda : label_apply.destroy())
        else:
            label_error = Label(self.frame_setting, text="Error type data", font=get_font(14), fg="red")
            label_error.place(x=150, y=300)
            label_error.after(2000, lambda : label_error.destroy())
        
        
    def create_setting_window(self):
    
        label_typeFile = Label(self.frame_setting, text="Type File", font=get_font(12))
        label_typeFile.grid(row=0, column=0)
        radio_xml = Radiobutton(self.frame_setting, text=".xml", font=get_font(12), variable=self.TypeFile_var, value=0)
        radio_xml.grid(row=1, column=0)
        radio_json = Radiobutton(self.frame_setting, text=".json", font=get_font(12), variable=self.TypeFile_var, value=1)
        radio_json.grid(row=2, column=0)
        
        label_min_quantity_rain = Label(self.frame_setting, text="Min quantity rain", font=get_font(12))
        label_min_quantity_rain.grid(row=3, column=0)
        min_quantity_rain_box = Entry(self.frame_setting, textvariable=self.min_quantity_rain_var)
        min_quantity_rain_box.delete(0, END)
        min_quantity_rain_box.insert(0, self.dict_limit["min_quantity_rain"])
        min_quantity_rain_box.grid(row=3, column=1)
        label_max_quantity_rain = Label(self.frame_setting, text="Max quantity rain", font=get_font(12))
        label_max_quantity_rain.grid(row=4, column=0)
        max_quantity_rain_box = Entry(self.frame_setting, textvariable=self.max_quantity_rain_var)
        max_quantity_rain_box.delete(0, END)
        max_quantity_rain_box.insert(0, self.dict_limit["max_quantity_rain"])
        max_quantity_rain_box.grid(row=4, column=1)
        
        label_min_quantity_water = Label(self.frame_setting, text="Min quantity water", font=get_font(12))
        label_min_quantity_water.grid(row=5, column=0)
        min_quantity_water_box = Entry(self.frame_setting, textvariable=self.min_quantity_water_var)
        min_quantity_water_box.delete(0, END)
        min_quantity_water_box.insert(0, self.dict_limit["min_quantity_water"])
        min_quantity_water_box.grid(row=5, column=1)
        label_max_quantity_water = Label(self.frame_setting, text="Max quantity water", font=get_font(12))
        label_max_quantity_water.grid(row=6, column=0)
        max_quantity_water_box = Entry(self.frame_setting, textvariable=self.max_quantity_water_var)
        max_quantity_water_box.delete(0, END)
        max_quantity_water_box.insert(0, self.dict_limit["max_quantity_water"])
        max_quantity_water_box.grid(row=6, column=1)
        
        label_min_temperature = Label(self.frame_setting, text="Min temperature", font=get_font(12))
        label_min_temperature.grid(row=7, column=0)     
        min_temperature_box = Entry(self.frame_setting, textvariable=self.min_temperature_var)
        min_temperature_box.delete(0, END)
        min_temperature_box.insert(0, self.dict_limit["min_temperature"])
        min_temperature_box.grid(row=7, column=1)
        label_max_temperature = Label(self.frame_setting, text="Max temperature", font=get_font(12))
        label_max_temperature.grid(row=8, column=0)
        max_temperature_box = Entry(self.frame_setting, textvariable=self.max_temperature_var)
        max_temperature_box.delete(0, END)
        max_temperature_box.insert(0, self.dict_limit["max_temperature"])
        max_temperature_box.grid(row=8, column=1)
        
        label_min_humidity = Label(self.frame_setting, text="Min humidity", font=get_font(12))
        label_min_humidity.grid(row=9, column=0)     
        min_humidity_box = Entry(self.frame_setting, textvariable=self.min_humidity_var)
        min_humidity_box.delete(0, END)
        min_humidity_box.insert(0, self.dict_limit["min_humidity"])
        min_humidity_box.grid(row=9, column=1)
        label_max_humidity = Label(self.frame_setting, text="Max humidity", font=get_font(12))
        label_max_humidity.grid(row=10, column=0)
        max_humidity_box = Entry(self.frame_setting, textvariable=self.max_humidity_var)
        max_humidity_box.delete(0, END)
        max_humidity_box.insert(0, self.dict_limit["max_humidity"])
        max_humidity_box.grid(row=10, column=1)
        
        Button_Apply = Button(self.frame_setting, text="Apply", font=get_font(12), command=self.set_value)
        Button_Apply.place(x=50, y=300)
        Button_reset = Button(self.frame_setting, text="Reset to default", font=get_font(12), command=self.reset)
        Button_reset.place(x=50, y=350)        
        
        Label_read = Label(self.frame_setting, text=f"read file {self.typefile}", font=get_font(12))
        Label_read.place(x=800, y=500)
        
    def reset(self):
        def destroy_label():
            label_reset.destroy()
        
        self.set_default()
        label_reset = Label(self.frame_setting, text="Reset Success", font=get_font(14), fg="green")
        label_reset.place(x=150, y=300)
        label_restart = Label(self.frame_setting, text="Need to restart app", font=get_font(14), fg="#cc3300")
        label_restart.place(x=330, y=300)
        button_restart = Button(self.frame_setting, text="Restart")
        button_restart.place(x=330, y=350)
        label_reset.after(2000, destroy_label)
        
    def get_time(self):
        return self.df["date_time"][self.id]

    def get_quantity_rain(self):
        return self.df["quantity_rain"][self.id]

    def get_quantity_water(self):
        return self.df["quantity_water"][self.id]

    def get_temperature(self):
        return self.df["temperature"][self.id]

    def get_humidity(self):
        data = self.df["humidity"][self.id]
        self.id += 1
        return data

    def get_station_data(self, id):
        parentList = []
        if int(self.df["hardware_fail"][id]) == 1:
            parentList.append(id)
            parentList.append(self.df["date_time"][id])
            parentList.append("Hardware Fail")
            return parentList
        
        elif int(self.df["hardware_fail"][id]) != 1:
            parentList.append(id)
            parentList.append(self.df["date_time"][id])
            parentList.append("Normal")
            return parentList
        
        
    def get_station_id(self):
        station_id = self.station_id
        self.station_id += 1
        return station_id
    
    def get_graphId(self):
        graph_id = self.graph_id
        self.graph_id += 1
        return graph_id
    
    def get_iid(self):
        iid_var = self.iid
        self.iid += 1
        return iid_var

    def get_index_id(self):
        index_var = self.index_id
        self.index_id += 1
        return index_var

    def insert_child(self, min, max, keys, i, j):
        list_child = []
        if int(self.df[keys[j]][i]) < min:
            list_child.append(self.df["date_time"][i])
            list_child.append("lower the limit")
            list_child.append(self.list_keys[j])
            return list_child
        elif int(self.df[keys[j]][i]) > max:
            list_child.append(self.df["date_time"][i])
            list_child.append("higher the limit")
            list_child.append(self.list_keys[j])
            return list_child
        else: return list_child

    def get_parent_data(self, id, child_data):
        parent_data = []
        if len(child_data) != 0:
            parent_data.append(len(child_data))
            parent_data.append(id)
            if len(child_data) < 3 and len(child_data) > 0:
                parent_data.append("Low level")
            elif len(child_data) >= 3:
                parent_data.append("High level")
        elif len(child_data) == 0:
            parent_data.append(len(child_data))
            parent_data.append(id)
            parent_data.append("Normal")
        self.tree_id += 1
        return parent_data
    
    def get_insert_parent(self):
        id_in_insert = self.id_in_insert
        self.id_in_insert += 1
        return id_in_insert

    def get_child_data(self, i):
        list_child = []
        for j in range(1, len(self.df.keys())):
            if j == 1:
                child_data = self.insert_child(int(self.dict_limit["min_quantity_rain"]), int(self.dict_limit["max_quantity_rain"]), self.list_keys, i, j)
                if len(child_data) != 0:
                    list_child.append(child_data)
            elif j==2:
                child_data = self.insert_child(int(self.dict_limit["min_quantity_water"]), int(self.dict_limit["max_quantity_water"]), self.list_keys, i, j)
                if len(child_data) != 0:
                    list_child.append(child_data)
            elif j==3:
                child_data = self.insert_child(int(self.dict_limit["min_temperature"]), int(self.dict_limit["max_temperature"]), self.list_keys, i, j)
                if len(child_data) != 0:
                    list_child.append(child_data)
            elif j==4:
                child_data = self.insert_child(int(self.dict_limit["min_humidity"]), int(self.dict_limit["max_humidity"]), self.list_keys, i, j)
                if len(child_data) != 0:
                    list_child.append(child_data)
        return list_child
    
    def get_df(self, typefile):
        if typefile == ".xml\n":
            self.df = self.get_dataframe_xml()
        elif typefile == ".json\n":
            self.df = self.get_dataframe_json()
        else:
            self.df = self.get_dataframe_xml()
        
    def transform_xml(self, xml_doc):
        attr = xml_doc.attrib
        for xml in xml_doc.iter("data"):
            dict = attr.copy()
            dict.update(xml.attrib)

            yield dict
    
    def get_dataframe_json(self):
        with open("data/Simulate_dataJSON_v1.json", "r") as file_json:
            data = json.load(file_json)
            dataframe_json = pd.DataFrame(data)
            dataframe_json.set_index("id", inplace=True)
            return dataframe_json
    
    def get_dataframe_xml(self):
        tree = et.parse("data/Simulate_dataXML.xml")
        root = tree.getroot()
        trans = self.transform_xml(root)
        root_Dataframe = pd.DataFrame(trans)
        root_Dataframe.set_index("id", inplace=True)
        return root_Dataframe

