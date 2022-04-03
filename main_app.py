from pdb import Restart
from tkinter import *
from numpy import char
from get_data import *
from constant import *
from tkinter import ttk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


def search():
    id_search = var_id.get()
    id_search -= 1
    if id_search < 8640:
        child_data = keys.get_child_data(id_search)
        parent_data = keys.get_parent_data(id_search, child_data)
        Label_parent.config(text=f"id : {id_search+1} | Amount : {parent_data[0]} | Type : {parent_data[2]}")
    else : Label_parent.config(text="Out of range")

def reload_data():
    var_time = keys.get_time()
    var_quantity_rain = keys.get_quantity_rain()
    var_quantity_water = keys.get_quantity_water()
    var_temperature = keys.get_temperature()
    var_humidity = keys.get_humidity()
    button_time.configure(text=str(var_time))
    button_quantity_rain.configure(text=str(var_quantity_rain))
    button_quantity_water.configure(text=str(var_quantity_water))
    button_temperature.configure(text=str(var_temperature))
    button_humidity.configure(text=str(var_humidity))
    button_time.after(2000, reload_data)



dict_type = {}
window = Tk()
window.title("My App")
window.geometry("1024x600")
window.resizable(False, False)

my_notebook = ttk.Notebook(window)
my_notebook.pack()


frame_p1 = LabelFrame(my_notebook, width=1024, height=600)
frame_p2 = LabelFrame(my_notebook, width=1024, height=600)
frame_p3 = LabelFrame(my_notebook, width=1024, height=600)
frame_setting = LabelFrame(my_notebook, width=1024, height=600)
frame_p1.pack(fill="both", expand=1)
frame_p2.pack(fill="both", expand=1)
frame_p3.pack(fill="both", expand=1)
frame_setting.pack(fill="both", expand=1)


my_notebook.add(frame_p1, text="Show Data")
my_notebook.add(frame_p2, text="Historical Data")
my_notebook.add(frame_p3, text="Alarm Station")
my_notebook.add(frame_setting, text="Setting")

keys = Provider(frame_setting, window)

# Frame_p1

label_time = Label(frame_p1, text="Time", font=get_font(14))
label_time.grid(row=0, column=0, padx=20, pady=20)
label_quantity_rain = Label(frame_p1, text="Quantity Rain\n(millimeter)", font=get_font(14))
label_quantity_rain.grid(row=0, column=1, padx=20, pady=20)
label_quantity_water = Label(frame_p1, text="Quantity Water\n(meters)", font=get_font(14))
label_quantity_water.grid(row=0, column=2, padx=20, pady=20)
label_temperature = Label(frame_p1, text="Temperature\n(Celsius)", font=get_font(14))
label_temperature.grid(row=0, column=3, padx=20, pady=20)
label_humidity = Label(frame_p1, text="Humidity\n(percent)", font=get_font(14))
label_humidity.grid(row=0, column=4, padx=20, pady=20)


button_time = Button(frame_p1, font=get_font(14), padx=40, pady=5)
button_time.grid(row=1, column=0, sticky="nsew")
button_quantity_rain = Button(frame_p1, font=get_font(14), padx=40, pady=5)
button_quantity_rain.grid(row=1, column=1, sticky="nsew")
button_quantity_water = Button(frame_p1, font=get_font(14), padx=40, pady=5)
button_quantity_water.grid(row=1, column=2, sticky="nsew")
button_temperature = Button(frame_p1, font=get_font(14), padx=40, pady=5)
button_temperature.grid(row=1, column=3, sticky="nsew")
button_humidity = Button(frame_p1, font=get_font(14), padx=40, pady=5)
button_humidity.grid(row=1, column=4, sticky="nsew")


analog_tree = ttk.Treeview(frame_p1, height=15)
analog_tree["column"] = ("Amount", "Id", "Type")

analog_tree.column("#0", width=20, minwidth=25)
analog_tree.column("Amount", anchor=W, width=120)
analog_tree.column("Id", anchor=CENTER, width=150)
analog_tree.column("Type", anchor=W, width=120)

analog_tree.heading("#0", text="", anchor=W)
analog_tree.heading("Amount", text="Amount", anchor=W)
analog_tree.heading("Id", text="Id", anchor=CENTER)
analog_tree.heading("Type", text="Type", anchor=W)

for i in range(len(keys.df)):
    child_data = keys.get_child_data(i)
    parent_data = keys.get_parent_data(keys.tree_id, child_data)
    if len(child_data) != 0:
        keys.parent_id = keys.iid
        analog_tree.insert(parent="", index="end", iid=keys.get_iid(), text="", value=(parent_data[0], parent_data[1], parent_data[2]))
        keys.index_id = 0
        for j in range(len(child_data)):
            keys.child_id = keys.iid
            analog_tree.insert(parent="", index="end", iid=keys.get_iid(), text="", values=(child_data[j][0], child_data[j][1], child_data[j][2]))
            analog_tree.move(keys.child_id, keys.parent_id, keys.get_index_id())

analog_tree.place(x=100, y=170)


var_id = IntVar()
label_search = Label(frame_p1, text="Search", font=get_font(12))
label_search.place(x=600, y=170)
label_id = Label(frame_p1, text="id", font=get_font(12), padx=20)
label_id.place(x=550, y=197)
entry_search = Entry(frame_p1, textvariable=var_id)
entry_search.place(x=600, y=200)
button_search = Button(frame_p1, text="Search", command=search)
button_search.place(x=600, y=230)
Label_parent = Label(frame_p1, text="")
Label_parent.place(x=600, y=300)

Label_read = Label(frame_p1, text=f"read file {keys.typefile}", font=get_font(12))
Label_read.place(x=800, y=500)


reload_data()

# Frame_p2

    
def tap1():
    dict_keyWord = {
        "quantity_rain_ylabel":"Quantity rain(millimater)",
        "quantity_rain_title":"Graph quantity rain",
        "quantity_rain_label":"Quantity rain",
        "quantity_water_ylabel":"Quantity water(meters)",
        "quantity_water_title":"Graph quantity water",
        "quantity_water_label":"Quantity water",
        "temperature_ylabel":"Temperature(Celsius)",
        "temperature_title":"Graph temperature",
        "temperature_label":"Temperature",
        "humidity_ylabel":"Humidity(percent)",
        "humidity_title":"Graph humidity",
        "humidity_label":"Humidity"
    }
    
    def setValueGraph_quantity_rain():
        nameGraph_var = "quantity_rain"
        showGraph(nameGraph_var)
    
    def setValueGraph_quantity_water():
        nameGraph_var = "quantity_water"
        showGraph(nameGraph_var)
        
    def setValueGraph_temperature():
        nameGraph_var = "temperature"
        showGraph(nameGraph_var)
        
    def setValueGraph_humidity():
        nameGraph_var = "humidity"
        showGraph(nameGraph_var)
        
    def showGraph(name_request):
        
        def goBack():
            Button_disable.destroy()
            labelFrame_graph.destroy()
            tap1()
        
        def create_graph():
            for i in range(len(keys.df)):
                x_data.append(keys.df["date_time"][i])
                y_data.append(int(keys.df[name_request][i]))
                
            fig = plt.figure(figsize=(10, 6), dpi=100)
            plot1 = fig.add_subplot(111)
            plot1.plot(x_data, y_data, marker="", color="blue", label=dict_keyWord[f"{name_request}_label"])
            plot1.set_xlabel("Time")
            plot1.set_ylabel(dict_keyWord[f"{name_request}_ylabel"])
            plot1.set_title(dict_keyWord[f"{name_request}_title"])
            plot1.set_xticks([keys.df["date_time"][0], keys.df["date_time"][len(keys.df)-1]])
            plot1.legend(loc=2)
            plot1.grid()
            canv = FigureCanvasTkAgg(fig, master=labelFrame_graph)
            canv.draw()
            get_widz = canv.get_tk_widget()
            get_widz.pack()
        
        x_data = []
        y_data = []
        
        
        Button_graph_quantity_rain.destroy()
        Button_graph_quantity_water.destroy()
        Button_graph_quantity_temperature.destroy()
        Button_graph_quantity_humidity.destroy()
        Label_read.destroy()
        
        
        Button_disable = Button(frame_p2, text="Disable graph", command=goBack)
        Button_disable.pack(pady=5)
        labelFrame_graph = LabelFrame(frame_p2, text="Graph")
        labelFrame_graph.pack(fill="both", expand="yes", padx=10, pady=10)
        
        create_graph()
        

    Button_graph_quantity_rain = Button(frame_p2, text="Show graph quantity rain", command=setValueGraph_quantity_rain)
    Button_graph_quantity_rain.place(x=200, y=20)
    Button_graph_quantity_water = Button(frame_p2, text="Show graph quantity water", command=setValueGraph_quantity_water)
    Button_graph_quantity_water.place(x=350, y=20)
    Button_graph_quantity_temperature = Button(frame_p2, text="Show graph temperature", command=setValueGraph_temperature)
    Button_graph_quantity_temperature.place(x=510, y=20)
    Button_graph_quantity_humidity = Button(frame_p2, text="Show graph humidity", command=setValueGraph_humidity)
    Button_graph_quantity_humidity.place(x=660, y=20)
    Label_read = Label(frame_p2,text=f"read file {keys.typefile}", font=get_font(12))
    Label_read.place(x=800, y=500)

tap1()

# frame_p3

LabelFrame_tree = LabelFrame(frame_p3, text="Alarm")
LabelFrame_tree.pack(fill="both", expand="yes", padx=20, pady=20)
LabelFrame_search = LabelFrame(frame_p3, text="Search")
LabelFrame_search.pack(fill="both", expand="yes", padx=20, pady=20)
station_tree = ttk.Treeview(LabelFrame_tree)
station_tree["column"] = ("Id", "Time", "Type")

station_tree.column("#0", width=20, minwidth=25)
station_tree.column("Id", anchor=W,  width=120)
station_tree.column("Time", anchor=CENTER,  width=150)
station_tree.column("Type", anchor=W,  width=120)

station_tree.heading("#0", text="", anchor=W)
station_tree.heading("Id", text="Id", anchor=W)
station_tree.heading("Time", text="Time", anchor=CENTER)
station_tree.heading("Type", text="Type", anchor=W)

for i in range(len(keys.df)):
    if int(keys.df["hardware_fail"][i]) == 1:
        parent_list = keys.get_station_data(i)
        station_tree.insert(parent="", index="end", iid=keys.get_station_id(), text="", values=(parent_list[0], parent_list[1], parent_list[2]))
    
station_tree.pack(fill="both", expand="yes")


def Search_hardware_fail():
    id = id_var.get()
    if id >= 8640:
        station_search.configure(text="Out of range")
    else:
        parent_list = keys.get_station_data(id)
        station_search.configure(text=f"id : {parent_list[0]} | Time : {parent_list[1]} | Type : {parent_list[2]}")


LabelSearch = Label(LabelFrame_search, text="Search", font=get_font(12))
LabelSearch.place(x=10, y=10)
id_var = IntVar()
SearchBox = Entry(LabelFrame_search, textvariable=id_var)
SearchBox.place(x=10, y=40)
Button_submit = Button(LabelFrame_search, text="Search", font=get_font(10), command=Search_hardware_fail)
Button_submit.place(x=150, y=35)
station_search = Label(LabelFrame_search, text="", font=get_font(10))
station_search.place(x=10, y=70)
Label_read = Label(frame_p3, text=f"read file {keys.typefile}", font=get_font(12))
Label_read.place(x=800, y=500)


# frame_setting
        
keys.create_setting_window()
    
window.mainloop()