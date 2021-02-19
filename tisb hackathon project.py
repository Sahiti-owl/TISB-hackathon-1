#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
from tkinter import ttk
from tkinter import *
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import statistics  
import math
from PIL import Image, ImageTk
from datetime import date
import os

file_path = "C:/Users/aparna/Downloads/energy_consumption_2021_Sahiti.csv"
file_data = pd.read_csv(file_path)
months = ['January','February', 'March','April','May','June','July','August','September','October','November','December']
numbers_to_month = {1:'January', 2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
key = {'January': 1, 'February': 2, 'March':3, 'April':4, 'May': 5, 'June': 6, 'July': 7, 'August':8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

villa_no = 1
current_date = date.today()
month = numbers_to_month[current_date.month]
electricity_dict = {}
water_dict={}

 
def generate_green_score():
    x = 0.9
    y = 2.1
    electricity_scores = []
    water_scores = []
        
    for month in months:
        monthwise_electricity = file_data.loc[(file_data['Month'] == month)]
        monthwise_electricity["rank"]=monthwise_electricity.Electricity_per_person.rank(pct = True)
        electricity_scores.append(monthwise_electricity.loc[(monthwise_electricity['HouseID']==villa_no), "rank"].values[0])
        monthwise_water = file_data.loc[(file_data['Month'] == month)]
        monthwise_water["rank"]=monthwise_water.Water_per_person.rank(pct = True)
        water_scores.append(monthwise_water.loc[(monthwise_water['HouseID']==villa_no), "rank"].values[0])
     
        for x in range(1, len(monthwise_electricity)+1):
            green_score = (monthwise_electricity.loc[(monthwise_electricity['HouseID']==x), "rank"].values[0] +monthwise_water.loc[(monthwise_water['HouseID']==x), "rank"].values[0])/2
            green_score = green_score*100
            file_data.loc[(file_data['HouseID']==x) & (file_data['Month']==month),"Green_score"]= round((100-green_score),2)
            os.remove("C:/Users/aparna/Downloads/energy_consumption_2021_Sahiti.csv")
            file_data.to_csv("C:/Users/aparna/Downloads/energy_consumption_2021_Sahiti.csv", index = False)

def submitButtonFunction(people_entry, vehicles_entry):
   
    file_data = pd.read_csv("C:/Users/aparna/Downloads/energy_consumption_2021_Sahiti.csv")
    people_data = people_entry.get()
    vehicles_data = vehicles_entry.get()
    if len(vehicles_data)>0:
        file_data.loc[(file_data['HouseID'] == villa_no) & (file_data['Month'] == month),"Num_Green_Vehicles"]= vehicles_data
        print(file_data)
    if len(people_data)>0:
        file_data.loc[(file_data['HouseID'] == villa_no) & (file_data['Month'] == month),"Num_People"]= people_data
        print(file_data)
    os.remove("C:/Users/aparna/Downloads/energy_consumption_2021_Sahiti.csv")
    file_data.to_csv("C:/Users/aparna/Downloads/energy_consumption_2021_Sahiti.csv", index = False)
    
    
def create_plot_1():
    global file_data
    global villa_no
    file_data.query('HouseID == @villa_no ', inplace = True)
 
    graph = plt.figure(figsize=(12, 4))
    sns.barplot(x=file_data['Month'], y=file_data['Electricity'])
    
    plt.xlabel("Months")
    plt.title("Electricity")
    return graph

def create_plot_3():
    global file_data
    global villa_no
    file_data.query('HouseID == @villa_no ', inplace = True)
 
    graph = plt.figure(figsize=(12, 4))
    sns.barplot(x=file_data['Month'], y=file_data['Water'])
    
    plt.xlabel("Months")
    plt.title("Water")
    return graph

def createPredictionsTab(container):
    global months
    electricity_store = []
    water_store = []
    green_score_store=[]
   
    canvas = tk.Canvas(container)
    scrollable_frame = Frame(canvas,highlightbackground="green", highlightcolor="green", highlightthickness=8, width=500, height=500, bd= 0, padx = 100)
    yscrollbar = ttk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
    xscrollbar = ttk.Scrollbar(canvas, orient="horizontal", command=canvas.xview)
    scrollable_frame.bind("<Configure>",canvas.configure(scrollregion=canvas.bbox("all")) )

    yscrollbar.pack(side="right", fill="y")
    xscrollbar.pack(side="bottom", fill="y")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=yscrollbar.set)
    canvas.configure(xscrollcommand=xscrollbar.set)
    canvas.config(height = 650, width = 1100)
    
    for month in months:
        per_month_elec = file_data.loc[(file_data['HouseID'] == villa_no) & (file_data['Month'] == month),["Electricity"]].values[0]
        electricity_store.append(per_month_elec)
        per_month_water = file_data.loc[(file_data['HouseID'] == villa_no) & (file_data['Month'] == month),["Water"]].values[0]
        water_store.append(per_month_water)
        per_month_green_score = file_data.loc[(file_data['HouseID'] == villa_no) & (file_data['Month'] == month),["Green_score"]].values[0]
        green_score_store.append(per_month_green_score)
    electricity_mean = sum(electricity_store)/len(electricity_store)
    water_mean = sum(water_store)/len(water_store)
    green_score_mean = sum(green_score_store)/len(green_score_store)
    electricity_var = [(x-electricity_mean)**2 for x in electricity_store]
    electricity_std = math.sqrt(sum(electricity_var)/len(electricity_var))
    electricity_ste = electricity_std/(math.sqrt(len(electricity_store)))
    upper_electricity = electricity_mean + 1.96*electricity_ste
    lower_electricity = electricity_mean - 1.96*electricity_ste
    fig = create_plot_1()
    canvas_1 = FigureCanvasTkAgg(fig, scrollable_frame)  
    canvas_1.get_tk_widget().pack()
    
    electricity_prediction = Label(scrollable_frame, text = "Your predicted electricity for next month is in the range of : " + str(round(lower_electricity[0],2)) +'-'+ str(round(upper_electricity[0],2)), fg = 'green', underline = 0)
    electricity_prediction.config(font=("Courier", 13))
    electricity_prediction.pack()  
    water_var = [(x-water_mean)**2 for x in water_store]
    water_std = math.sqrt(sum(water_var)/len(water_var))
    water_ste = water_std/(math.sqrt(len(water_store)))
    upper_water = water_mean + 1.96*water_ste
    lower_water = water_mean - 1.96*water_ste
    
    fig_2 = create_plot_3()
    canvas_2 = FigureCanvasTkAgg(fig_2, scrollable_frame)  
    canvas_2.get_tk_widget().pack()
    water_prediction = Label(scrollable_frame, text = "Your predicted water usage for next month is in the range of : " + str(round(lower_water[0],2)) +"-"+ str(round(upper_water[0],2)), fg = 'green', underline = 0 )
    water_prediction.config(font=("Courier", 13))
    water_prediction.pack()  
    green_score_var = [(x-green_score_mean)**2 for x in green_score_store]
    green_score_std = math.sqrt(sum(green_score_var)/len(green_score_var))
    green_score_ste = green_score_std/(math.sqrt(len(green_score_store)))
    upper_green_score = green_score_mean + 1.96*green_score_ste
    lower_green_score = green_score_mean - 1.96*green_score_ste
    fig_2 = create_plot_2()
    canvas_2 = FigureCanvasTkAgg(fig_2, scrollable_frame)  
    canvas_2.get_tk_widget().pack()
    green_score_prediction = Label(scrollable_frame, text = "Your predicted green score for next month is in the range of : " + str(round(lower_green_score[0],2)) +"-"+ str(round(upper_green_score[0],2)), fg = 'green', underline = 0 )
    green_score_prediction.config(font=("Courier", 13))
    green_score_prediction.pack()
    
    scrollable_frame.pack(side="left", fill="both", expand=True)
    canvas.pack(side="left", fill="both", expand=True)

    
def create_plot_2():
    global file_data
    global villa_no
    file_data.query('HouseID == @villa_no ', inplace = True)
 
    graph = plt.figure(figsize=(12, 4))
    sns.barplot(x=file_data['Month'], y=file_data['Green_score'])
    
    plt.xlabel("Months")
    plt.title("Green scores")
    return graph

def create_electricity_neighborplot():
    global electricity_dict
    people_electricity_data =file_data["Electricity"].tolist()
    electricity_average = sum(people_electricity_data)/ len(people_electricity_data)
    personal_data = file_data.loc[(file_data['HouseID'] == villa_no),["Electricity"]].values
    personal_average = list(sum(personal_data)/len(personal_data))
    electricity_dict = {"You":personal_average, "Neighbor average": electricity_average}
    electricity_dataframe = pd.DataFrame(electricity_dict)
    
    graph = plt.figure(figsize =(12,2))
    sns.barplot(data = electricity_dataframe, orient = "h")
    plt.title("Electricity: You vs Neighbors")
    
    return graph

def create_water_neighborplot():
    global water_dict
    people_water_data =file_data["Water"].tolist()
    water_average = sum(people_water_data)/ len(people_water_data)
    personal_data = file_data.loc[(file_data['HouseID'] == villa_no),["Water"]].values
    personal_average = list(sum(personal_data)/len(personal_data))
    water_dict = {"You":personal_average, "Neighbor average": water_average}
    water_dataframe = pd.DataFrame(water_dict)
    
    graph = plt.figure(figsize =(12,2))
    sns.barplot(data = water_dataframe, orient = "h")
    plt.title("Water usage: You vs Neighbors")
    return graph



def createMainTab(container):
    canvas = tk.Canvas(container)
    scrollable_frame = Frame(canvas,highlightbackground="green", highlightcolor="green", highlightthickness=8, width=500, height=500, bd= 0, padx = 100)
    yscrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    xscrollbar = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)

    scrollable_frame.bind(
        "<Configure>",  canvas.configure(scrollregion=canvas.bbox("all")))
        
    yscrollbar.pack(side="right", fill="y")
    xscrollbar.pack(side="bottom", fill="y")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=yscrollbar.set)
    canvas.configure(xscrollcommand=xscrollbar.set)
    canvas.config(height = 650, width = 1100)


    
    
    label = tk.Label(scrollable_frame, text = 'Villa ' +str(villa_no) + " green report", fg = "green", height = 2, anchor ='n', underline = 8)
    label.config(font=("Courier", 44))
    label.pack()
    
    month_label = tk.Label(scrollable_frame, text = 'Month: ' + month , fg = "green", height = 2, anchor ='n', underline = 8)
    month_label.config(font=("Courier", 20))
    month_label.pack()

    electricity_label = tk.Label(scrollable_frame, text = 'Electricity:' + str(round(electricity[0],2))+' kilowatts', fg = "green", underline = 0, anchor = 'w')
    electricity_label.config(font = ("Courier", 20))
    electricity_label.pack()

    water_label = tk.Label(scrollable_frame, text = "Water usage:" + str(round(water[0],2))+' litres', fg = 'green', underline = 0, anchor = 'w')
    water_label.config(font=("Courier", 20))
    water_label.pack()

    green_score_label = tk.Label(scrollable_frame, text = "green score:" + str(score[0]), fg = 'green', underline = 0, anchor = 'w')
    green_score_label.config(font=("Courier", 20))
    green_score_label.pack()

    if score[0]>0 and score[0]<35:
        describe_score = 'Bad'
    elif score[0]>35 and score[0]<55:
        describe_score = 'Satisfactory'
    elif score[0]>55 and score[0]<75:
        describe_score = 'Good'
    elif score[0]>75 and score[0]<90:
        describe_score = 'Great!'
    else:
        describe_score = 'EXCELLENT!!!'
        
    general_label = tk.Label(scrollable_frame, text = "green score is " + describe_score, fg = 'green', underline = 0, anchor = 'w')
    general_label.config(font=("Courier", 20))
    general_label.pack()

    #levels_image_path = Image.open("C:/Users/aparna/Desktop/levels.png")
    #levels_image_path = levels_image_path.resize((200,130),Image.ANTIALIAS)
    #test = ImageTk.PhotoImage(levels_image_path)

    #levels_image = Label(scrollable_frame,image=test)
    #levels_image.image = test
    #levels_image.pack()
    
    fig_electric = create_electricity_neighborplot()
    canvas_5 = FigureCanvasTkAgg(fig_electric, scrollable_frame)  
    canvas_5.get_tk_widget().pack()
    
    if electricity_dict["You"][0]> electricity_dict["Neighbor average"]:
        electricity_average_label = Label(scrollable_frame, text = "Your electricity usage is "+ str(round(electricity_dict["You"][0]-electricity_dict["Neighbor average"]))+" kilowatts greater than your average neighbor's")
    else:
        electricity_average_label = Label(scrollable_frame, text = "Your electricity usage is "+ str(round(electricity_dict["Neighbor average"]-electricity_dict["You"][0]))+" kilowatts less than your average neighbor's")
        
    electricity_average_label.config(font=("Courier", 13), fg = "green")
    electricity_average_label.pack()  
    
    fig_water = create_water_neighborplot()
    canvas_6 = FigureCanvasTkAgg(fig_water, scrollable_frame)  
    canvas_6.get_tk_widget().pack()
    
    if water_dict["You"][0]> water_dict["Neighbor average"]:
        water_average_label = Label(scrollable_frame, text = "Your water usage is "+ str(round(water_dict["You"][0]-water_dict["Neighbor average"]))+" litres greater than your average neighbor's")
    else:
        water_average_label = Label(scrollable_frame, text = "Your water usage is "+ str(round(water_dict["Neighbor average"]-water_dict["You"][0]))+" litres less than your average neighbor's")
        
    water_average_label.config(font=("Courier", 13), fg="green")
    water_average_label.pack()
    scrollable_frame.pack(side="left", fill="both", expand=True)
    canvas.pack(side="left", fill="both", expand=True)



def createUpdateTab(update_container):
    update_canvas = tk.Canvas(update_container)
    update_frame = Frame(update_canvas,highlightbackground="green", highlightcolor="green", highlightthickness=8, width=500, height=500, bd= 0, padx = 100)
    update_yscrollbar = ttk.Scrollbar(update_canvas, orient="vertical", command=update_canvas.yview)
    update_xscrollbar = ttk.Scrollbar(update_canvas, orient="horizontal", command=update_canvas.xview)
    update_frame.bind("<Configure>",update_canvas.configure(scrollregion=update_canvas.bbox("all")) )

    update_yscrollbar.pack(side="right", fill="y")
    update_xscrollbar.pack(side="bottom", fill="y")
    x0 = update_frame.winfo_screenwidth()/2
    y0 = update_frame.winfo_screenheight()/2
    update_canvas.create_window((x0, y0), window=update_frame, anchor="center")
    update_canvas.configure(yscrollcommand=update_yscrollbar.set)
    update_canvas.configure(xscrollcommand=update_xscrollbar.set)
    update_canvas.config(height = 650, width = 1100)
    
    people_label = Label(update_frame, text = 'Number of people')
    people_label.pack()
    people_entry = Entry(update_frame)
    people_entry.pack()
    vehicles_label = Label(update_frame, text = 'Number of green vehicles')
    vehicles_label.pack()
    vehicles_entry = Entry(update_frame)
    vehicles_entry.pack()
    submit = Button(update_frame, text = "submit", command = lambda:submitButtonFunction(people_entry, vehicles_entry))
    submit.pack()
    
    
    update_frame.pack()
    update_canvas.pack(side="left", fill="both", expand=True)
    

def createLeaderboardTab(leaderboard_container):
    global file_data
    leaderboard_canvas = tk.Canvas(leaderboard_container)
    leaderboard_frame = LabelFrame(leaderboard_canvas)
    treeview_table = ttk.Treeview(leaderboard_frame)
    
    #treescrolly = Scrollbar(leaderboard_frame, orient = 'vertical',command = treeview_table.yview)
    #treeview_table.configure(yscrollcommand = treescrolly.set)
    #treeview_table["displaycolumns"]= ("HouseID", "Year")
    #treescrolly.pack(side = "right", fill= "y")
    leaderboard_yscrollbar = ttk.Scrollbar(leaderboard_canvas, orient="vertical", command=leaderboard_canvas.yview)
    leaderboard_xscrollbar = ttk.Scrollbar(leaderboard_canvas, orient="horizontal", command=leaderboard_canvas.xview)
    leaderboard_frame.bind("<Configure>",leaderboard_canvas.configure(scrollregion=leaderboard_canvas.bbox("all")) )

    leaderboard_yscrollbar.pack(side="right", fill="y")
    leaderboard_xscrollbar.pack(side="bottom", fill="y")
    leaderboard_canvas.create_window((0, 0), window=leaderboard_frame, anchor="nw")
    leaderboard_canvas.configure(yscrollcommand=leaderboard_yscrollbar.set)
    leaderboard_canvas.configure(xscrollcommand=leaderboard_xscrollbar.set)
    leaderboard_canvas.config(height = 650, width = 1100)
    
    leaderboard_data = file_data[['HouseID','Month','Green_score']]
    leaderboard_data = leaderboard_data.sort_values('Green_score', ascending=False)
    print(leaderboard_data)
    
    treeview_table["column"]= list(leaderboard_data.columns)
    treeview_table["show"]="headings"
    treeview_table.column("#1", anchor="center", stretch=YES)
    treeview_table.column("#2", anchor="center", stretch=YES)
    treeview_table.column("#3", anchor="center", stretch=YES)
    treeview_table.pack(fill=BOTH, expand=True)
    for column in treeview_table["column"]:
        treeview_table.heading(column, text = column)
    table_data = leaderboard_data.to_numpy().tolist()
    for row in table_data[0:15]:
        treeview_table.insert("","end",values= row)

       
    leaderboard_frame.pack(side="left", fill="both", expand=True)
    leaderboard_canvas.pack(side="left", fill="both", expand=True)
    
    
generate_green_score()
electricity = file_data.loc[(file_data['HouseID'] == villa_no) & (file_data['Month'] == month),["Electricity"]].values[0]

water = file_data.loc[(file_data['HouseID'] == villa_no) & (file_data['Month'] == month),["Water"]].values[0]
score = file_data.loc[(file_data['HouseID'] == villa_no) & (file_data['Month'] == month),["Green_score"]].values[0]

root = tk.Tk()
#container = ttk.Frame(root)

notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)
notebook.pressed_index = None
container = ttk.Frame(notebook)
predictions_container = ttk.Frame(notebook)
update_container = ttk.Frame(notebook)
leaderboard_container = ttk.Frame(notebook)
container.pack()
predictions_container.pack()
update_container.pack()
leaderboard_container.pack()
notebook.add(update_container, text="Update Profile")
notebook.add(leaderboard_container, text="Leaderboard")
notebook.add(container, text="Green Report")
notebook.add(predictions_container, text="Predictions")


createLeaderboardTab(leaderboard_container)
createMainTab(container)
createPredictionsTab(predictions_container)
createUpdateTab(update_container)
 
print('score',score)

root.mainloop()
