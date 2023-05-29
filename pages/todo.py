from tkinter import *
from tkinter.messagebox import *
import datetime
from tkcalendar import Calendar
import re
import sqlite3

root = Tk()
root.title("TaskVault")
root.resizable(False, False)
root.geometry("1400x671")

bg = PhotoImage(file="img/Planned.gif")
my_label = Label(root, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    text TEXT,
                    date TEXT,
                    option TEXT,
                    price TEXT
                )''')

conn.commit()
conn.close()
conn_planned = sqlite3.connect('planned_items.db')
cursor_planned = conn_planned.cursor()

cursor_planned.execute('''CREATE TABLE IF NOT EXISTS planned_items (
                            id INTEGER PRIMARY KEY,
                    text TEXT,
                    date TEXT,
                    option TEXT,
                    price TEXT
                )''')

conn_planned.commit()
conn_planned.close()

def AddFunc(txt, index=END):
    global add, price
    add = Tk()
    add.title('Add your Purchases')
    add.geometry('500x500')
    add.resizable(width=False, height=False)
    add.config(background='#FFF')

    frame = Frame(add)
    frame.pack()
    label = Label(frame, font=("Arial Bold", 30))
    label.pack(side=LEFT)
    options = ['Health', 'Food', 'Entertainment', 'Shopping', 'Sport', 'Indispensabilities']
    variable = StringVar(frame)
    variable.set(options[0])
    dropdown = OptionMenu(frame, variable, *options)
    dropdown.pack(side=LEFT)

    price_label = Label(add, text='Price:', font=(ft, 20), bg='#FFF')
    price_label.pack(pady=10)
    price_entry = Entry(add, font=(ft, 16, ''), validate="key")
    price_entry.pack()

    def validate_price_entry(new_value):
        if not new_value:
            return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    vcmd = add.register(validate_price_entry)
    price_entry.config(validatecommand=(vcmd, '%P'))

    cal = Calendar(label, selectmode='day', date_pattern='d/m/y')
    cal.pack(side=RIGHT)

    global Write
    Write = Text(add, font=(ft, 16, ''))
    Write.insert(END, txt)
    Write.pack()

    w, h = 7, 1
    bConfirm = Button(add,
                      text='Confirm',
                      width=w, height=h, bd=0, highlightthickness=0,
                      font=(ft, 20), fg='#FFF',
                      bg='#00a32e', command=lambda: addTask(index))
    bConfirm.place(x=384, y=450)

    def selectDate(date):
        global selected_date
        selected_date = date

    def addTask(index):
        text = Write.get('1.0', END)
        price = price_entry.get()
        if text.strip() == '':
            showerror('Error', 'Please enter a purchase to confirm.')
        elif price.strip() == '':
            showerror('Error', 'Please enter a price to confirm.')
        else:
            selected_date = cal.selection_get().strftime('%d/%m/%Y')
            selected_option = variable.get()
            task = f"{text.strip()} ({selected_date}) {selected_option} - {price.strip()}"
            Planned.insert(index, task)
            add.destroy()

            text, date_option_price = task.rsplit("(", 1)
            text = text.strip()
            date, option_price = date_option_price.split(")", 1)
            date = date.strip()
            option, price = option_price.split("-", 1)
            option = option.strip()
            price = price.strip()

            conn_planned = sqlite3.connect('planned_items.db')
            cursor_planned = conn_planned.cursor()
            cursor_planned.execute("INSERT INTO planned_items (text, date, option, price) VALUES (?, ?, ?, ?)",
                                (text, date, option, price))
            conn_planned.commit()
            conn_planned.close()

            currency_symbol = "€" 

            try:
                conn_currency = sqlite3.connect('currency.db') 
                cursor_currency = conn_currency.cursor()

                cursor_currency.execute("SELECT symbol FROM currency")
                result = cursor_currency.fetchone()

                if result is not None:
                    currency_symbol = result[0]
            except sqlite3.Error as e:
                print(f"Error accessing currency database: {e}")
            finally:
                if conn_currency:
                    conn_currency.close()

            task_with_currency = f"{text} ({selected_date}) {selected_option} - {price}{currency_symbol}"

            conn_planned = sqlite3.connect('planned_items.db')
            cursor_planned = conn_planned.cursor()
            cursor_planned.execute("UPDATE planned_items SET price = ? || ' ' || ? WHERE text = ? AND date = ? AND option = ? AND price = ?",
                                (price, currency_symbol, text, date, option, price))
            conn_planned.commit()
            conn_planned.close()

            Planned.delete(index)
            Planned.insert(index, task_with_currency)

    add.mainloop()

selected_date = None
def Edit():
    global selected_date
    if Planned.curselection():
        index = Planned.curselection()[0]
        task = Planned.get(index)
        if '(' in task and ')' in task:
            old_date = re.findall(r'\((.*?)\)', task)[0]
            task = task.split('-')[0].strip()
            option = task.split()[-1]
            task = task.replace(f" {option}", "").strip()
            task = task.replace(f" ({old_date})", "")
        else:
            old_date = None

        if old_date is not None:
            conn_planned = sqlite3.connect('planned_items.db')
            cursor_planned = conn_planned.cursor()
            cursor_planned.execute("DELETE FROM planned_items WHERE text = ? AND date = ?",
                                   (task, old_date))
            conn_planned.commit()
            conn_planned.close()

        Planned.delete(index)
        AddFunc(task, index)
        selected_date = None
    else:
        showerror('Error', 'Please select a task to edit')

def DeleteP():
    itemToDelete = Planned.curselection()
    if itemToDelete:
        index = itemToDelete[0]
        taskToDelete = Planned.get(index)

        text, date_option_price = taskToDelete.rsplit("(", 1)
        text = text.strip()

        Planned.delete(index)

        conn_planned = sqlite3.connect('planned_items.db')
        cursor_planned = conn_planned.cursor()
        cursor_planned.execute("DELETE FROM planned_items WHERE text=?", (text,))
        conn_planned.commit()
        conn_planned.close()
    else:
        showerror('Error', 'You should select a purchase')

def DeleteE():
    itemToDelete = Expense.curselection()
    if itemToDelete:
        index = itemToDelete[0]
        taskToDelete = Expense.get(index)

        text, date_option_price = taskToDelete.rsplit("(", 1)
        text = text.strip()

        Expense.delete(index)

        conn_expenses = sqlite3.connect('expenses.db')
        cursor_expenses = conn_expenses.cursor()
        cursor_expenses.execute("DELETE FROM expenses WHERE text=?", (text,))
        conn_expenses.commit()
        conn_expenses.close()
    else:
        showerror('Error', 'You should select a purchase from the Expense list')
def ClearTS():
    TSsize = Planned.size()
    if TSsize > 0:
        yesNo = askyesno('Warning', 'Are you sure you want to clear all purchases?')
        if yesNo:
            Planned.delete(0, END)

            conn_planned = sqlite3.connect('planned_items.db')
            cursor_planned = conn_planned.cursor()
            cursor_planned.execute("DELETE FROM planned_items")
            conn_planned.commit()
            conn_planned.close()
        else:
            pass
    else:
        showwarning('Warning', 'Purchases are already cleared')

def ClearTA():
    TAsize = Expense.size()
    if TAsize > 0:
        yesNo = askyesno('Warning', 'Are you sure you want to clear all purchases')
        if yesNo:
            Expense.delete(0, END)

            conn = sqlite3.connect('expenses.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses")
            conn.commit()
            conn.close()
        else:
            pass
    else:
        showwarning('Warning', 'Purchases are already clear')


def Finish():
    itemToFinish = Planned.curselection()
    if itemToFinish:
        index = itemToFinish[0]
        textToFinish = Planned.get(index)
        Expense.insert(END, textToFinish)
        Planned.delete(index)

        text, date_option_price = textToFinish.rsplit("(", 1)
        text = text.strip()
        date, option_price = date_option_price.split(")", 1)
        date = date.strip()
        option, price = option_price.split("-", 1)
        option = option.strip()
        price = price.strip()

        conn_planned = sqlite3.connect('planned_items.db')
        cursor_planned = conn_planned.cursor()
        cursor_planned.execute("DELETE FROM planned_items WHERE text=?", (text,))
        conn_planned.commit()
        conn_planned.close()

        conn_expenses = sqlite3.connect('expenses.db')
        cursor_expenses = conn_expenses.cursor()
        cursor_expenses.execute("INSERT INTO expenses (text, date, option, price) VALUES (?, ?, ?, ?)",
                                (text, date, option, price))
        conn_expenses.commit()
        conn_expenses.close()
    else:
        showerror('Error', 'You should select a purchase')


def Redo():
    itemToRedo = list(Expense.curselection())
    if len(itemToRedo) != 0:
        textToRedo = Expense.get(itemToRedo)
        Planned.insert(END, textToRedo)
        Expense.delete(itemToRedo)

        text, date_option_price = textToRedo.rsplit("(", 1)
        text = text.strip()
        date, option_price = date_option_price.split(")", 1)
        date = date.strip()
        option, price = option_price.split("-", 1)
        option = option.strip()
        price = price.strip()

        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE text = ? AND date = ? AND option = ? AND price = ?",
                       (text, date, option, price))
        conn.commit()
        conn.close()

        conn_planned = sqlite3.connect('planned_items.db')
        cursor_planned = conn_planned.cursor()
        cursor_planned.execute("INSERT INTO planned_items (text, date, option, price) VALUES (?, ?, ?, ?)",
                               (text, date, option, price))
        conn_planned.commit()
        conn_planned.close()
    else:
        showerror('Error', 'You should select a purchase')

def LoadExpenses():
    conn_expenses = sqlite3.connect('expenses.db')
    cursor_expenses = conn_expenses.cursor()
    cursor_expenses.execute("SELECT * FROM expenses")
    rows = cursor_expenses.fetchall()
    for row in rows:
        text = f"{row[1]} ({row[2]}) {row[3]} - {row[4]}"
        Expense.insert(END, text)
    
    conn_expenses.close()

def LoadPlannedItems():
    conn_planned = sqlite3.connect('planned_items.db')
    cursor_planned = conn_planned.cursor()
    cursor_planned.execute("SELECT * FROM planned_items")
    rows = cursor_planned.fetchall()
    for row in rows:
        text = f"{row[1]} ({row[2]}) {row[3]} - {row[4]}"
        Planned.insert(END, text)
    conn_planned.close()

# Here we declare 4 variables
w,h,b,ft=994,700,'#FFF','Century Gothic'

global Planned
PlCanv = Canvas(root, bg='#1AA4F6')
ExCanv = Canvas(root, bg='#8aff70')
Planned = Listbox(PlCanv, bd=2, relief='solid', width=25, height=15, font=(ft, 17, ''), highlightcolor='#0f0', selectmode=BROWSE)
Expense = Listbox(ExCanv, bd=2, relief='solid', width=25, height=15, font=(ft, 17, ''), highlightcolor='#0f0', selectmode=BROWSE)

LoadPlannedItems()
LoadExpenses()

scXS = Scrollbar(PlCanv, orient=HORIZONTAL, bg='#1AA4F6', command=Planned.xview)
scXA = Scrollbar(ExCanv, orient=HORIZONTAL, command=Expense.xview)
scYS = Scrollbar(PlCanv, orient=VERTICAL, command=Planned.yview)
scYA = Scrollbar(ExCanv, orient=VERTICAL, command=Expense.yview)

Planned.configure(xscrollcommand=scXS.set, yscrollcommand=scYS.set)
Expense.configure(xscrollcommand=scXA.set, yscrollcommand=scYA.set)


scXS.pack(side=BOTTOM,fill=X)
scXA.pack(side=BOTTOM,fill=X)
scYS.pack(side=RIGHT,fill=Y)
scYA.pack(side=RIGHT,fill=Y)
Planned.pack()
Expense.pack()
PlCanv.place(x=33,y=160)
ExCanv.place(x=425,y=160)

def set_scrollregion(event=None):
    Planned.configure(scrollregion=Planned.bbox("all"))
    Expense.configure(scrollregion=Expense.bbox("all"))

def on_mousewheel(event):
    if event.delta > 0:
        Planned.yview_scroll(-1, "units")
        Expense.yview_scroll(-1, "units")
    elif event.delta < 0:
        Planned.yview_scroll(1, "units")
        Expense.yview_scroll(1, "units")

Planned.bind("<Configure>", set_scrollregion)
Expense.bind("<Configure>", set_scrollregion)
Planned.bind("<MouseWheel>", on_mousewheel)
Expense.bind("<MouseWheel>", on_mousewheel)

IAdd = PhotoImage(file='img/eAdd.gif')
IEdit = PhotoImage(file='img/eEdit.gif')
IDelete = PhotoImage(file='img/Edelete.gif')
I2Delete = PhotoImage(file='img/Edelete.gif')
IClear = PhotoImage(file='img/eClear.gif')
IRedo = PhotoImage(file='img/eRedo.gif')
IFinished = PhotoImage(file='img/eCheck.gif')
ISave = PhotoImage(file= 'img/Esave.gif')
IOpen = PhotoImage(file='img/Eopen.gif')
I2Save = PhotoImage(file= 'img/Esave.gif')
I2Clear = PhotoImage(file='img/eClear2.gif')

BDelete = Button(root,width=41,height=40,image=IDelete,bd=0,highlightthickness=0, command=DeleteP)
bDelete = Button(root,width=41,height=40,image=IDelete,bd=0,highlightthickness=0, command=DeleteE)
BClear = Button(root,width=42,height=57,image=IClear,bd=0,highlightthickness=0, command=ClearTS)
bClear = Button(root,width=42,height=55,image=I2Clear,bd=0,highlightthickness=0, command=ClearTA)
BAdd = Button(root,width=42,height=44,image=IAdd,command=lambda:AddFunc(''),bd=0,highlightthickness=0)
BFinished = Button(root,width=41,height=41,image=IFinished,bd=0,highlightthickness=0, command=Finish)
BRedo = Button(root,width=41,height=44,image=IRedo,bd=0,highlightthickness=0, command=Redo)
BEdit = Button(root,width=40,height=43,image=IEdit,bd=0,highlightthickness=0, command=Edit)


BClear.place(x=335,y=610)
bClear.place(x=720,y=610)
BAdd.place(x=32,y=107)
BEdit.place(x=188,y=108)
BDelete.place(x=104,y=110)
bDelete.place(x=425,y=110)
BFinished.place(x=335,y=111)
BRedo.place(x=262,y=107)


root.mainloop()