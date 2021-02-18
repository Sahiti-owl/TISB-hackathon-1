#!/usr/bin/env python
# coding: utf-8

# In[64]:


import tkinter as tk
from tkinter import ttk
from tkinter import *
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

file_path = "C:/Users/aparna/Downloads/energy_consumption_2020_Sahiti.csv"
file_data = pd.read_csv(file_path)

def my_function():
    canvas.configure(scrollregion=canvas.bbox("all"))
    


def raise_frame(frame):
    frame.tkraise()
    

def update():
    raise_frame(update_frame)
    update_frame.pack()
    

key = {'January': 1, 'February': 2, 'March':3, 'April':4, 'May': 5, 'June': 6, 'July': 7, 'August':8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

villa_no = 1
month = 'January'
electricity = file_data.loc[(file_data['HouseID'] == villa_no) & (file_data['Month'] == month),["Electricity"]].values[0]

water = file_data.loc[(file_data['HouseID'] == villa_no) & (file_data['Month'] == month),["Water"]].values[0]
#score = file_data.loc[(file_data['HouseID'] == villa_no) & (file_data['Month'] == month),["Green_Score"]].values[0]


root = tk.Tk()
container = ttk.Frame(root)
container.pack()

canvas = tk.Canvas(container)
scrollable_frame = Frame(canvas,highlightbackground="green", highlightcolor="green", highlightthickness=8, width=500, height=500, bd= 0, padx = 100)
yscrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
xscrollbar = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)

def cancel():
    raise_frame(scrollable_frame)
    scrollable_frame.pack()

def bind(event):
    canvas.yview_scroll(-1*(event.delta/120), "units")

scrollable_frame.bind(
    "<Configure>",
    my_function()
)

yscrollbar.pack(side="right", fill="y")
xscrollbar.pack(side="bottom", fill="y")
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=yscrollbar.set)
canvas.configure(xscrollcommand=xscrollbar.set)
canvas.config(height = 650, width = 1100)


label = tk.Label(scrollable_frame, text = str(villa_no) + " green report", fg = "green", height = 2, anchor ='n', underline = 8)
label.config(font=("Courier", 44))
label.pack()

electricity_label = tk.Label(scrollable_frame, text = 'electricity:' + str(electricity), fg = "green", underline = 0, anchor = 'w')
electricity_label.config(font = ("Courier", 20))
electricity_label.pack()

water_label = tk.Label(scrollable_frame, text = "water usage:" + str(water), fg = 'green', underline = 0, anchor = 'w')
water_label.config(font=("Courier", 20))
water_label.pack()

#green_score_label = tk.Label(scrollable_frame, text = "green score:" + str(score), fg = 'green', underline = 0, anchor = 'w')
#green_score_label.config(font=("Courier", 20))
#green_score_label.pack()

general_label = tk.Label(scrollable_frame, text = "green score is________ than last months showing _______", fg = 'green', underline = 0, anchor = 'w', height = 2)
general_label.config(font=("Courier", 20))
general_label.pack()

update = tk.Button(scrollable_frame, text = "UPDATE DETAILS",bg = "green", anchor = 'center', command=update)
update.config(font = ("Courier", 15))
update.pack()


update_frame = Frame(canvas,  width=500, height=500, bd= 0, padx = 100)

people_label = Label(update_frame, text = 'Number of people')
people_label.pack()
people_entry = Entry(update_frame)
people_entry.pack()
vehicles_label = Label(update_frame, text = 'Number of green vehicles')
vehicles_label.pack()
vehicles_entry = Entry(update_frame)
vehicles_entry.pack()
submit = Button(update_frame, text = "submit", command =submit)
submit.pack()
cancel = Button(update_frame, text = "cancel", command = cancel)
cancel.pack()
print(file_data)

def submit():
    global people_entry
    global vehicles_entry
    global file_data
    people_data = people_entry.get()
    vehicles_data = vehicles_entry.get()
    if len(vehicles_data)>0:
        file_data.loc[(file_data['HouseID'] == villa_no) & (file_data['Month'] == month),"Num_Green_Vehicles"]= vehicles_data
    if len(people_data)>0:
        file_data.loc[(file_data['HouseID'] == villa_no) & (file_data['Month'] == month),"Num_People"]= people_data
    print(file_data)
    raise_frame(scrollable_frame)
    scrollable_frame.pack()

numbers_to_month = {1:'January', 2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
green_scores=[]
def generate_green_score():
    x = 0.9
    y = 2.1
    electricity_scores = []
    months = ['January','February', 'March','April','May','June','July','August','September','October','November','December']
    for month in months:
        monthwise_electricity = file_data.loc[(file_data['Month'] == month)]
        monthwise_electricity["rank"]=monthwise_electricity.Electricity_per_person.rank(pct = True)
        electricity_scores.append(monthwise_electricity.loc[(monthwise_electricity['HouseID']==villa_no), "rank"].values[0])
    print(electricity_scores[1])
    water_scores = []
    for month in months:
        monthwise_water = file_data.loc[(file_data['Month'] == month)]
        monthwise_water["rank"]=monthwise_water.Water_per_person.rank(pct = True)
        water_scores.append(monthwise_water.loc[(monthwise_water['HouseID']==villa_no), "rank"].values[0])
    print(water_scores)
    for num in range(0,12):
        print(electricity_scores[num])
        green_score = electricity_scores[num]*x + water_scores[num]*y
        print(green_score)
        this_month = numbers_to_month[num+1]
        file_data.loc[(file_data['HouseID']==villa_no) & (file_data['Month']==this_month),"Green_score"]= green_score
        
        

    
generate_green_score()
def create_plot_1():
    global file_data
    global villa_no
    file_data.query('HouseID == @villa_no ', inplace = True)
 
    graph = plt.figure(figsize=(12, 6))
    sns.lineplot(x=file_data['Month'], y=file_data['Green_score'])
    
    plt.xlabel("Months")
    plt.title("Green scores")
    return graph
fig = create_plot()
canvas_1 = FigureCanvasTkAgg(fig, scrollable_frame)  
canvas_1.get_tk_widget().pack()

def create_plot_2():
    global file_data
    global villa_no
    file_data.query('HouseID == @villa_no ', inplace = True)
 
    graph = plt.figure(figsize=(12, 6))
    sns.barplot(x=file_data['Month'], y=file_data['Green_score'])
    
    plt.xlabel("Months")
    plt.title("Green scores")
    return graph
fig_2 = create_plot()
canvas_2 = FigureCanvasTkAgg(fig_2, scrollable_frame)  
canvas_2.get_tk_widget().pack()

canvas.pack(side="left", fill="both", expand=True)



root.mainloop()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




