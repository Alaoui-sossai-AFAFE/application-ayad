import tkinter as tk
from tkinter import Scrollbar
from tkcalendar import Calendar, DateEntry
from tkinter import PhotoImage
import time
import sqlite3

conn = sqlite3.connect("dates.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS selected_dates (date TEXT)")
conn.commit()
conn.close()

def select_date():
    day = cal.get_date()
    selected_dates_listbox.insert(0, day)
    save_date_to_database(day)

def clear_dates():
    selected_dates_listbox.delete(0, tk.END)
    clear_listbox()
    clear_database()

def save_date_to_database(day):
    conn = sqlite3.connect("dates.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO selected_dates (date) VALUES (?)", (day,))
    conn.commit()
    conn.close()

def clear_listbox():
    selected_dates_listbox.delete(0, tk.END)

def clear_database():
    conn = sqlite3.connect("dates.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM selected_dates")
    conn.commit()
    conn.close()

def load_dates_from_database():
    conn = sqlite3.connect("dates.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date FROM selected_dates")
    dates = cursor.fetchall()
    conn.close()

    for date in dates:
        selected_dates_listbox.insert(0, date[0])

root = tk.Tk()
root.geometry("445x642")
root.resizable(False, False)
root.title("Calendar")

bg = PhotoImage(file="img/clouds.gif")
my_label = tk.Label(root, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

cal = Calendar(root, selectmode='day', date_pattern='dd/MM/yyyy')
cal.place(x=70, y=100, width=300, height=200)

selected_dates_listbox = tk.Listbox(root)
selected_dates_listbox.place(x=157, y=307, width=120, height=200)

scrollbar = Scrollbar(root)
scrollbar.place(x=260, y=307, height=200)
selected_dates_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=selected_dates_listbox.yview)

select_button = tk.Button(root, text="Select", command=select_date)
select_button.place(x=220, y=520)

clear_button = tk.Button(root, text="Clear", command=clear_dates)
clear_button.place(x=170, y=520)

load_dates_from_database()

clock_label = tk.Label(root, font=('Open Sans Light', 23, 'bold'), bg='#243B4A', fg='#FFFFFF')
clock_label.place(x=20, y=20, width=120)

def update_clock():
    current_time = time.strftime('%H:%M')
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock)

update_clock()

root.mainloop()
