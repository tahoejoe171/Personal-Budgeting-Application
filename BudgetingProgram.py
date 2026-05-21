#BUDGETING LEDGER PROGRAM

import tkinter as tk
from matplotlib.patches import Patch
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import traceback
from tkinter import ttk
from tkinter import *
import pandas as pd
from datetime import datetime
import csv
from decimal import Decimal 

#create root tkinter object
FILE_NAME = "ledger.csv"
#create global csv on file. to be updated with each submission so that the balance can be read
try:
       ledger = pd.read_csv(FILE_NAME)
       ledger["Date"] = pd.to_datetime(ledger["Date"], format="%Y-%m-%d %H:%M:%S.%f")

except Exception as e:
    print("Error is:",e)
    #Create Ledger CSV (if missing) with appropriate labels, as well as 
        #total balance and spending limits per category
        #Limits: Rent, Gas, Groceries, Utilities, Entertainment, Food, Other, 401k/investment, and Total Limit
            #The datetime object in pandas only accepts about 1970+- 587 years due to the 64 bit integer limit in seconds. Thus the initialized dummy date for unused entries is 1900-01-01 00:00:00 (so pd.to_datetime() works properly)
    data = [['Interaction Type','Source','Amount','Name','Category','Date'],
            ['Balance','',0,'','',datetime(1900, 1, 1, 0, 0, 0.000000)],
            ['Limit','',0,'','Rent',datetime(1900, 1, 1, 0, 0, 0.000000)],
            ['Limit','',0,'','Gas',datetime(1900, 1, 1, 0, 0, 0.000000)],
            ['Limit','',0,'','Groceries',datetime(1900, 1, 1, 0, 0, 0.000000)],
            ['Limit','',0,'','Utilities',datetime(1900, 1, 1, 0, 0, 0.000000)],
            ['Limit','',0,'','Entertainment',datetime(1900, 1, 1, 0, 0, 0.000000)],
            ['Limit','',0,'','Food',datetime(1900, 1, 1, 0, 0, 0.000000)],
            ['Limit','',0,'','Other',datetime(1900, 1, 1, 0, 0, 0.000000)],
            ['Limit','',0,'','Investments',datetime(1900, 1, 1, 0, 0, 0.000000)],
            ['Limit','',0,'','Total Limit',datetime(1900, 1, 1, 0, 0, 0.000000)]]
    with open("Ledger.csv", mode="w",newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
    ledger = pd.read_csv(FILE_NAME, parse_dates=["Date"])
    ledger["Date"] = pd.to_datetime(ledger["Date"], format="%Y-%m-%d %H:%M:%S.%f")
root=tk.Tk()
root.title("Budgeting Program")
root.geometry("800x800")
root.title("Budgeting Ledger")

#create continer for two frames
container = tk.Frame(root)
container.pack(fill="both", expand = True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

#create two main root frames
frame_enter_transaction = tk.Frame(container,bg="light blue")
frame_visualization = tk.Frame(container, bg="light blue")
frame_visualization.grid(sticky="nsew")
frame_enter_transaction.grid(row=0,column=0,sticky="nsew")

#These booleans tell the analysis functions if they need to redraw the graph (Which should be done if update_balance() is called)
a1 = False
a2 = False
a3 = False


#update balance label (add an if clause to see if the bal_label amount equals the balance in the csv, and call this function if not. That way
#it only reads the csv when absolutely necessary, wait no thats dumb because why would you submit new transactions of $0?)

def update_balance():
    try:
        global ledger
        ledger = pd.read_csv(FILE_NAME)
        ledger["Date"] = pd.to_datetime(ledger["Date"], format="%Y-%m-%d %H:%M:%S.%f")
        withdrawals = -1*(ledger.loc[ledger["Interaction Type"]=="Withdrawal","Amount"].astype(float).sum())
        deposits = ledger.loc[ledger["Interaction Type"]=="Deposit","Amount"].astype(float).sum()
        bal_label.config(text=f'Balance: ${round(Decimal(withdrawals+deposits),2)}')
        ledger.iloc[0,2] = int(bal_label.text)
        a1 = False
        a2 = False
        a3 = False


    except Exception:
        (traceback.print_exc())


#create root Nav menu 
menu = tk.Menu(root)
menu.add_command(label="Enter Transaction", command = lambda: frame_enter_transaction.tkraise())
def raise_and_update_balance():
        update_balance()
        frame_visualization.tkraise()
menu.add_command(label="Visualize", command = lambda: raise_and_update_balance())
root.config(menu=menu)

#create/configure Visualization and Transaction Frames
tk.Label(frame_enter_transaction, text="Enter your information to begin", bg="light blue").grid(row=0,column=frame_enter_transaction.grid_size()[0]//2,sticky="nesw")
tk.Label(frame_visualization, text="Click visualization optins to begin", bg="light blue").grid(row=0,column=0,sticky="EW", columnspan=3)

frame_visualization.grid_columnconfigure(2, weight=1)
frame_enter_transaction.grid_rowconfigure(2, weight=1)
frame_enter_transaction.grid_columnconfigure(0, weight=1)






#Visualization Frame

    #Create Balance Label
try:
    bal_label = tk.Label(frame_visualization, text=f'Balance: {pd.read_csv(FILE_NAME, parse_dates=["Date"]).iloc[0, 2]}', bg = 'light blue')
    bal_label.grid(row=1,column=0, sticky="NEW", columnspan = 3)
except:
    bal_label = tk.Label(frame_visualization, text=f'Balance: 0', bg="light blue")
    bal_label.grid(row=1,column=0, sticky="NEW", columnspan = 3)


    #Create visualization buttons

spending_by_category = tk.Button(frame_visualization, text="Spending by Category", command = lambda: analyze_spending_by_category())
spending_by_category.grid(row=2,column=0, sticky="EW")
spending_limits = tk.Button(frame_visualization, text="Spending Limits", command = lambda: analyze_spending_limits(datetime.now().month))
spending_limits.grid(row=2,column=1, sticky="EW")
spending_locations = tk.Button(frame_visualization, text="Spending Locations", command = lambda: analyze_spending_locations(datetime.now().month))
spending_locations.grid(row=2,column=2, sticky="EW")  
for col in range(3):
    frame_visualization.grid_columnconfigure(col, weight=1)

    #create viewing window that takes up rest of the screen with its row weight

frame_visualization.grid_rowconfigure(3, weight = 1)
a1_window = tk.Frame(frame_visualization, bg="white")
a1_window.grid(row=3,column=0, columnspan=3, sticky="NESW")
a2_window = tk.Frame(frame_visualization, bg="white")
a2_window.grid(row=3,column=0, columnspan=3, sticky="NESW")
a3_window = tk.Frame(frame_visualization, bg="white")
a3_window.grid(row=3,column=0, columnspan=3, sticky="NESW")


#sum spending over the past month in each category. display in pie chart

a1_window.tkraise() #default window
#A1_window (analysis 1 window)
    #boolean to check if the graph has already been created

#IMPROVE TO TAKE A TIMEFRAME ARGUMENT
def analyze_spending_by_category():
    global a1
    a2_window.lower()
    a3_window.lower()
    if  not a1:
        a1_window.tkraise()            
        categories = ["Rent","Gas","Groceries","Utilities","Entertainment","Food","Other","Investments"]
        sums = []
        for i in range(len(categories)):
            try: #Sum the "Amount"'s for each category of withdrawals this month
                x=(ledger.loc[(ledger["Category"]==categories[i]) & 
                              (ledger["Interaction Type"]=="Withdrawal") &
                              ((ledger["Date"].dt.month)==(datetime.now().month))
                              ,"Amount"].astype(float).sum())
                if x:
                    sums.append(x)
                else: 
                    sums.append(0)
                    categories[i] = "" #Only show category names with data in pie chart
            except:
                print("No Data for timeframe")
                return()
        # Create a Matplotlib Figure
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        def autopct_hide_zero(pct):
            return f"{pct:.0f}%" if pct > 0 else ""
        ax.pie(sums, labels =categories, autopct=autopct_hide_zero)
        ax.set_title(f"Spending by Category\nTotal: ${sum(sums):.2f}")

        # Embed figure into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=a1_window)  # A tk.DrawingArea
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        a1=True


#A2_window (analysis 2 window)
#IMPROVE TO TAKE MONTH/YEAR ARGUMENT
def analyze_spending_limits(month):
    global a2
    a1_window.lower()
    a3_window.lower() 
    if  not a2:
        a2_window.tkraise()
        #sum spending over the past month in each category. Compare to limits in a bar graph
        categories = ["Rent","Gas","Groceries","Utilities","Entertainment","Food","Other","Investments"]
        lims = ledger.iloc[0:9].loc[ledger["Interaction Type"]=="Limit","Amount"].astype(float).tolist()
        sums = []
        for i in range(len(categories)):
            try: #Sum the "Amount"'s for each category of withdrawals this month
                x=(ledger.loc[(ledger["Category"]==categories[i]) & 
                              (ledger["Interaction Type"]=="Withdrawal") &
                              ((ledger["Date"].dt.month)==(datetime.now().month))
                              ,"Amount"].astype(float).sum())
                if x:
                    sums.append(x)
                else: 
                    sums.append(0)
            except:
                print("No Data for timeframe")
                return()

        fig = Figure(figsize = (5,4),dpi=100)
        ax = fig.add_subplot(111)
        ax.set_title("Spending vs Spending Limits")
        limbars = ax.bar(categories, lims, label="Spending Limits", alpha=0.7, color='black')
        totbars = ax.bar(categories, sums, label="Total Spending", alpha=0.6, color='blue')
        
        for i in range(len(limbars)):
            if totbars[i].get_height()>limbars[i].get_height():
                height = totbars[i].get_height()
                ax.text((totbars[i].get_x() + totbars[i].get_width()/2), height, f'${(height):.2f}', ha='center',va='bottom',fontsize = 12, color="red")


        legend_elements = [
            Patch(facecolor="blue", label="Spent"),
            Patch(facecolor="gray", label="Limit"),
            Patch(facecolor="cornflowerblue", label="Exceeded Limit"),
        ]
        ax.legend(handles=legend_elements, fontsize=12, title="Spending")
        canvas = FigureCanvasTkAgg(fig, master=a2_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        a2=True



def analyze_spending_locations(timeframe):
    #sum spending over the past month in each location. Display in a pie chart
    #takes a timeframe argument(month, year, all time) and returns a pie chart of spending locations in that timeframe
    #currently takes the current month (found in the button command call)
    #FIX .unique().tolist() DOEsNT WORK
    global a3  
    a1_window.lower()
    a2_window.lower()
    if not a3:
        sums = []
        a3_window.tkraise()
        locations = ledger.loc[
            (ledger["Date"].dt.month == timeframe)&
            (ledger["Interaction Type"]=="Withdrawal"),
            "Source"].unique().tolist()
        if locations:
            for location in locations:
                sums.append(ledger.loc[
                            (ledger["Date"].dt.month==timeframe) &
                            (ledger["Interaction Type"]=="Withdrawal") &
                            (ledger["Source"]==location),
                            "Amount"].astype(float).sum())
        else:
            print("No Data for timeframe")
            return()
        # Create a Matplotlib Figure
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        def autopct_hide_zero(pct):
            return f"{pct:.0f}%" if pct > 0 else ""
        ax.pie(sums, labels =locations, autopct=autopct_hide_zero)
        ax.set_title(f"Spending by Location\nTotal: ${sum(sums):.2f}")
        # Embed figure into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=a3_window)  # A tk.DrawingArea
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


        a3=True
    pass

def analyze_dynamic_spending():
    #analyze trends in non-obligatory (non-static) spending categories
    pass    








#Transaction Frame


###### METHODS  ######

#Clears out all entry fields
def clear():
    try:
        for widget in dep_widgets:
            widget.destroy()
    except:
        pass
    dep_widgets.clear()

def update_limits():
    try:
        global ledger
        ledger = pd.read_csv(FILE_NAME, parse_dates=["Date"])
        ledger["Date"] = pd.to_datetime(ledger["Date"], format="%Y-%m-%d %H:%M:%S.%f")
        ledger.iloc[1,2]=float(rententry.get())
        ledger.iloc[2,2]=float(gasentry.get())
        ledger.iloc[3,2]=float(grocentry.get())
        ledger.iloc[4,2]=float(utilentry.get())
        ledger.iloc[5,2]=float(ententry.get())
        ledger.iloc[6,2]=float(foodentry.get())
        ledger.iloc[7,2]=float(otherentry.get())
        ledger.iloc[8,2]=float(inventry.get())
        ledger.iloc[9,2]=ledger.loc[ledger["Interaction Type"]=="Limit","Amount"].iloc[1:9].sum()
        ledger.to_csv(FILE_NAME, index=False)
        total_limit.text = (0,ledger.iloc[9,2])
    except Exception as e:
        print("fail ",e)
        pass

j=1 #row # for widgets 
dep_widgets = []
#adds a new row of item inputs
def add_item(frame):
    global j
    INLabel = tk.Label(frame,text="Item Name: ")
    INLabel.grid(row=j, column=0, sticky="nesw")
    dep_widgets.append(INLabel)
    INEntry = tk.Entry(frame)
    INEntry.grid(row=j, column=1, sticky="nesw")
    dep_widgets.append(INEntry)
    DALabel = tk.Label(frame,text="Dollar Amount: ")
    DALabel.grid(row=j, column=2, sticky="nesw")
    dep_widgets.append(DALabel)
    DAEntry = tk.Entry(frame)
    DAEntry.grid(row=j, column=3, sticky="nesw")
    dep_widgets.append(DAEntry)
    CLabel = tk.Label(frame, text="Category: ")
    CLabel.grid(row=j, column=4, sticky="nesw")
    dep_widgets.append(CLabel)
    DLabel = tk.Label(frame,text="Date:")
    DLabel.grid(row = j, column = 6, sticky = "nesw")
    dep_widgets.append(DLabel)
    DEntry = tk.Entry(frame)
    DEntry.grid(row = j, column = 7, sticky='nesw')
    dep_widgets.append(DEntry)

    if frame==frame_deposit:
        combo=ttk.Combobox(frame, values=["Select","Paycheck","Venmo","Bank Transfer","Other"])
        combo.grid(row=j, column=5, sticky="nesw")
        dep_widgets.append(combo)
        combo.set(combo_box.get())
        DEntry.delete(0,tk.END)
        DEntry.insert(0,date_entry.get())

        
    else:
        combo=ttk.Combobox(frame, values=["Select","Groceries","Gas","Food","Internet","Rent","Utilities","Other"])
        combo.grid(row=j, column=5, sticky="nesw")
        dep_widgets.append(combo)
        combo.set(combo_boxw.get())
        DEntry.delete(0,tk.END)
        DEntry.insert(0,date_entryw.get())
    j+=1

#Removes current item
def remove_item(frame):
    try:
        for i in range(1,9):
            global dep_widgets
            dep_widgets[-1].destroy()
            dep_widgets = dep_widgets[0:-1]
        global j
        j=j-1
    except Exception as e:
        print("fail ",e)
        pass

#Submits the data to the csv for storage and resets the page.
def submit(x):
    interaction_type="Withdrawal"
    source=scw.get()
    if x: #if deposit
        interaction_type="Deposit"
        source=sc.get()
        global ledger
        #read the ledger so correct types are in memory
        ledger = pd.read_csv(FILE_NAME, parse_dates=["Date"])
        ledger["Date"] = pd.to_datetime(ledger["Date"], format="%Y-%m-%d %H:%M:%S.%f")


    for i in range(int(len(dep_widgets)/8)):  
        if not (dep_widgets[(i*8+6)].get()):
            the_date = datetime.now()    
        else: 
            the_date = (str(dep_widgets[(i*8+6)].get()) + " 00:00:00.000000")
        the_date = pd.to_datetime(the_date, format="%Y-%m-%d %H:%M:%S.%f")
        ledger.loc[len(ledger)] = [interaction_type,
                                   source,
                                   float(dep_widgets[(i*8)+3].get()),
                                   dep_widgets[(i*8)+1].get().strip().capitalize(), 
                                   dep_widgets[(i*8+7)].get(), 
                                   the_date]
        #Update Balance (depending on if deposit or withdraw)
        if not x: #if withdraw (subtract from balance)
            ledger.iloc[0,2]-=float(dep_widgets[(i*8)+3].get())
        else: #if deposit (add to balance)
            ledger.iloc[0,2]+=float(dep_widgets[(i*8)+3].get())
    #return to blank slate
    clear()
    scw.delete(0,tk.END)
    sc.delete(0,tk.END)
    date_entry.delete(0,tk.END)
    date_entryw.delete(0,tk.END)
    combo_box.set("Select")
    combo_boxw.set("Select")
    ledger.to_csv(FILE_NAME, index=False)

def deposit():
    #clear the frame and make certain inputs appear which have their own functions
    frame_deposit.tkraise()
    dep_widgets.clear()


def withdraw():
    #clear the frame and make certain inputs appear which have their own functions
    frame_withdraw.tkraise()
    dep_widgets.clear()

def limits():
    frame_limits.tkraise()
    dep_widgets.clear()

###### Transaction Frame Initialization ######



#Create Deposit and Withdraw frames within Transaction Frame
frame_deposit = tk.Frame(frame_enter_transaction, bg="light blue")
frame_withdraw = tk.Frame(frame_enter_transaction, bg="light blue")
frame_limits = tk.Frame(frame_enter_transaction, bg="light blue")
frame_limits.grid(row=2,column=0, rowspan=4, columnspan=4, sticky="nesw")
frame_withdraw.grid(row=2,column=0, rowspan=4, columnspan=4, sticky="nesw")
frame_deposit.grid(row=2,column=0, rowspan=4, columnspan=4, sticky="nesw")

#Initialize Withdraw frame
tk.Label(frame_withdraw,text=" Reciever: ").grid(row=0, column=0, sticky="nesw")
scw=tk.Entry(frame_withdraw)
scw.grid(row=0, column=1, sticky="nesw")
tk.Label(frame_withdraw, text="Category: ").grid(row=0, column=2, sticky="nesw")
combo_boxw=ttk.Combobox(frame_withdraw, values=["Select","Groceries","Gas","Food","Internet","Rent","Utilities", "Entertainment","Investment","Other"])
combo_boxw.grid(row=0, column=3, sticky="nesw")
combo_boxw.set("Select")
date_labelw = tk.Label(frame_withdraw, text="Date:") 
date_labelw.grid(row=0, column=4, sticky="nesw")
date_entryw = tk.Entry(frame_withdraw, text="MM/DD/YYYY")
date_entryw.grid(row=0, column=5, sticky="nesw")
tk.Button(frame_withdraw,text="Add Item", command=lambda:add_item(frame_withdraw)).grid(row=0, column=6, sticky="nesw")
tk.Button(frame_withdraw,text="Remove Item", command=lambda:remove_item(frame_withdraw)).grid(row=0, column=8, sticky="nesw")
tk.Button(frame_withdraw,text="Clear Items", command=clear).grid(row=0, column=10, sticky="nesw")
tk.Button(frame_withdraw,text="Submit", command=lambda:submit(False)).grid(row=0, column=7, sticky="nesw")


#Initialize deposit frame
tk.Label(frame_deposit,text=" Source:   ").grid(row=0, column=0, sticky="nesw")
sc=tk.Entry(frame_deposit)
sc.grid(row=0, column=1, sticky="nesw")
tk.Label(frame_deposit, text="Category: ").grid(row=0, column=2, sticky="nesw")
combo_box=ttk.Combobox(frame_deposit, values=["Select","Paycheck","Venmo","Bank Transfer","Other"])
combo_box.grid(row=0, column=3, sticky="nesw")
combo_box.set("Select")
date_label = tk.Label(frame_deposit, text="Date:") 
date_label.grid(row=0, column=4, sticky="nesw")
date_entry = tk.Entry(frame_deposit, text="MM/DD/YYYY")
date_entry.grid(row=0, column=5, sticky="nesw")
tk.Button(frame_deposit,text="Add Item", command=lambda:add_item(frame_deposit)).grid(row=0, column=6, sticky="nesw")
tk.Button(frame_deposit,text="Remove Item", command=lambda:remove_item(frame_deposit)).grid(row=0, column=8, sticky="nesw")
tk.Button(frame_deposit,text="Clear Items", command=clear).grid(row=0, column=10, sticky="nesw")
tk.Button(frame_deposit,text="Submit", command=lambda:submit(True)).grid(row=0, column=7, sticky="nesw")



#initialize spending limits frame
rent_limit = tk.Label(frame_limits, text=f"Rent Limit:")
rent_limit.grid(row=0, column=0, sticky=f"nesw")
rentlim = tk.StringVar()
rentlim.set([f"{ledger.iloc[1,2]}"])
rententry = tk.Entry(frame_limits,textvariable = rentlim)
rententry.grid(row=0, column=1, sticky="nesw")

gas_limit = tk.Label(frame_limits, text=f"Gas Limit:")
gas_limit.grid(row=1, column=0, sticky=f"nesw")
gaslim = tk.StringVar()
gaslim.set([f"{ledger.iloc[2,2]}"])
gasentry = tk.Entry(frame_limits,textvariable = gaslim)
gasentry.grid(row=1, column=1, sticky="nesw")

groceries_limit = tk.Label(frame_limits, text=f"Groceries Limit:")
groceries_limit.grid(row=2, column=0, sticky=f"nesw")
groclim = tk.StringVar()
groclim.set([f"{ledger.iloc[3,2]}"])
grocentry = tk.Entry(frame_limits,textvariable = groclim)
grocentry.grid(row=2, column=1, sticky="nesw")

utilities_limit = tk.Label(frame_limits, text=f"Utilities Limit:")
utilities_limit.grid(row=3, column=0, sticky=f"nesw")
utillim = tk.StringVar()
utillim.set([f"{ledger.iloc[4,2]}"])
utilentry = tk.Entry(frame_limits,textvariable = utillim)
utilentry.grid(row=3, column=1, sticky="nesw")

entertainment_limit = tk.Label(frame_limits, text=f"Entertainment Limit:")
entertainment_limit.grid(row=4, column=0, sticky=f"nesw")
entlim = tk.StringVar()
entlim.set([f"{ledger.iloc[5,2]}"])
ententry = tk.Entry(frame_limits,textvariable = entlim)
ententry.grid(row=4, column=1, sticky="nesw")

food_limit = tk.Label(frame_limits, text=f"Food Limit:")
food_limit.grid(row=5, column=0, sticky=f"nesw")
foodlim = tk.StringVar()
foodlim.set([f"{ledger.iloc[6,2]}"])
foodentry = tk.Entry(frame_limits,textvariable = foodlim)
foodentry.grid(row=5, column=1, sticky="nesw")

other_limit = tk.Label(frame_limits, text=f"Other Limit:")
other_limit.grid(row=6, column=0, sticky=f"nesw")
otherlim = tk.StringVar()
otherlim.set([f"{ledger.iloc[7,2]}"])
otherentry = tk.Entry(frame_limits,textvariable = otherlim)
otherentry.grid(row=6, column=1, sticky="nesw")

investments_limit = tk.Label(frame_limits, text=f"Investments Limit:")
investments_limit.grid(row=7, column=0, sticky=f"nesw")
invlim = tk.StringVar()
invlim.set([f"{ledger.iloc[8,2]}"])
inventry = tk.Entry(frame_limits,textvariable = invlim)
inventry.grid(row=7, column=1, sticky="nesw")

try:
    total_limit = tk.Label(frame_limits, text=f'Total Budget Limit: ${ledger.loc[ledger["Interaction Type"]=="Limit", "Amount"].iloc[0:-1].sum():.2f}')
except: 
    total_limit = tk.Label(frame_limits, text="0")
total_limit.grid(row = 9, column=0, sticky='nesw')


update = tk.Button(frame_limits, text="Update Limits", command=lambda: update_limits())
update.grid(row=8,column=0, columnspan=2, sticky="nesw")


button_container = tk.Frame(frame_enter_transaction, bg="light blue")
button_container.grid(row=1,column=0,columnspan=4, sticky="nesw")
button_container.grid_columnconfigure(0, weight=1)
button_container.grid_columnconfigure(1, weight=1)
button_container.grid_columnconfigure(3, weight=1)
button_container.grid_columnconfigure(2, weight=1)
button_container.grid_columnconfigure(4, weight=1)
button_container.grid_columnconfigure(5, weight=1)
button_container.grid_columnconfigure(6, weight=1)

v=BooleanVar(value=True)
tk.Frame(button_container, bg="light blue").grid(row=1,column=0, sticky="nesw")
tk.Frame(button_container, bg="light blue").grid(row=1,column=2, sticky="nesw")
tk.Frame(button_container, bg="light blue").grid(row=1,column=4, sticky="nesw")
tk.Frame(button_container, bg="light blue").grid(row=1,column=6, sticky="nesw")
tk.Radiobutton(button_container,text="Deposit", variable = v, value=1, bg="light blue", command=lambda:deposit()).grid(row=1,column=1, sticky="NS")
tk.Radiobutton(button_container,text="Set Limits", variable = v, value=3,bg="light blue", command=lambda:limits()).grid(row=1,column=3,sticky = "NS")
tk.Radiobutton(button_container,text="Withdraw", variable = v, value=2,bg="light blue", command=lambda:withdraw()).grid(row=1,column=5, sticky="NS")


##### Program Initialization #####

frame_enter_transaction.tkraise()
#Default deposit selection
deposit()

root.mainloop()

