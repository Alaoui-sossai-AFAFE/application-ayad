from tkinter import*
from tkinter.messagebox import *
import datetime
from tkcalendar import Calendar
import re
import sqlite3

conn = sqlite3.connect('Todo.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT)")
conn.commit()
conn.close()

conn_done= sqlite3.connect('Done.db')
cursor_done = conn_done.cursor()
cursor_done.execute("CREATE TABLE IF NOT EXISTS done (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT)")
conn_done.commit()
conn_done.close()

root = Tk()
root.title("Todolist")
root.resizable(False, False)
root.geometry("800x671")

bg = PhotoImage(file="img/Todolist.gif")
my_label = Label(root, image = bg)
my_label.place(x=0, y=0, relwidth=1,relheight=1)

def AddFunc(txt,index=END):
    global add
    add = Tk()
    add.title('Add Note')
    add.geometry('500x400')
    add.resizable(width=False, height=False)
    add.config(background='#FFF')

    label = Label(add, font=("Arial Bold", 30))
    label.pack()

    cal = Calendar(label, selectmode='day', date_pattern ='d/m/y')
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
    bConfirm.place(x=384, y=350)

    def selectDate(date):
        global selected_date
        selected_date = date

    def addTask(index):
        global selected_date
        text = Write.get('1.0', END)
        if text.strip() == '':
            showerror('Error', 'Please enter a task to confirm.')
        else:
            task_text = text.strip()
            task_date = cal.selection_get().strftime('%d/%m/%Y')
            
            conn = sqlite3.connect('Todo.db')
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO todo (item) VALUES (?)", (f"{task_text} ({task_date})",))
            conn.commit()
            
            conn.close()
            
            tasksStarted.insert(index, f"{task_text} ({task_date})")
            
            add.destroy()

    add.mainloop()
def Edit():
    global selected_date
    if tasksStarted.curselection():
        index = tasksStarted.curselection()[0]
        task = tasksStarted.get(index)
        original_task = task  
        if '(' in task and ')' in task:
            old_date = re.findall(r'\((.*?)\)', task)[0]
            task = task.split('-')[0].strip()
            task = task.replace(f" ({old_date})", "")
        else:
            old_date = None
        if old_date is not None:
            conn = sqlite3.connect('Todo.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Todo WHERE item=?", (original_task,))
            conn.commit()
            conn.close()

        tasksStarted.delete(index)
        AddFunc(task, index)
        selected_date = None
    else:
        showerror('Error', 'Please select a task to edit')

def DeleteTS():
    selected_index = tasksStarted.curselection()
    if len(selected_index) == 0:
        showerror('Error', 'You must select at least one task')
    else:
        item_text = tasksStarted.get(selected_index[0])

        tasksStarted.delete(selected_index[0])

        conn = sqlite3.connect('Todo.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM todo WHERE item=?", (item_text,))
        conn.commit()

        conn.close()

def DeleteTA():
    itemToDelete = tasksAchieved.curselection()
    if itemToDelete:
        index = itemToDelete[0]
        taskToDelete = tasksAchieved.get(index)

        text, date_option_price = taskToDelete.rsplit("(", 1)
        text = text.strip()

        tasksAchieved.delete(index)

        conn_done = sqlite3.connect('Done.db')
        cursor_done = conn_done.cursor()
        cursor_done.execute("DELETE FROM done WHERE item=?", (taskToDelete,))
        conn_done.commit()
        conn_done.close()
    else:
        showerror('Error', 'You must select at least one task')
               
def ClearTS():
    TSsize = tasksStarted.size()
    if TSsize > 0:
        yesNo = askyesno('Warning', 'Are you sure you want to clear all tasks?')
        if yesNo:
            tasksStarted.delete(0, END)

            conn = sqlite3.connect('Todo.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Todo")
            conn.commit()
            conn.close()
        else:
            pass
    else:
        showwarning('Warning', 'Tasks are already clear')
def ClearTA(): 
    TAsize = tasksAchieved.size()
    if TAsize > 0:
        yesNo = askyesno('Warning', 'Are you sure you want to clear all tasks')
        if yesNo:
            tasksAchieved.delete(0, END)

            conn_done = sqlite3.connect('Done.db')
            cursor_done = conn_done.cursor()
            cursor_done.execute("DELETE FROM Done")
            conn_done.commit()
            conn_done.close()
        else:
            pass
    else:
        showwarning('Warning', 'Tasks are already clear')        
def Finish():
    itemToFinish = list(tasksStarted.curselection())
    if len(itemToFinish) != 0:
        textToFinish = tasksStarted.get(itemToFinish)
        tasksAchieved.insert(END, textToFinish)
        tasksStarted.delete(itemToFinish)

        # Connect to the Todo database
        conn = sqlite3.connect('Todo.db')
        cursor = conn.cursor()

        # Connect to the Done database
        conn_done = sqlite3.connect('Done.db')
        cursor_done = conn_done.cursor()

        cursor.execute("DELETE FROM todo WHERE item=?", (textToFinish,))
        conn.commit()

        cursor_done.execute("INSERT INTO done (item) VALUES (?)", (textToFinish,))
        conn_done.commit()

        conn.close()
        conn_done.close()
    else:
        showerror('Error', 'You should select a task')
def Redo():
    itemToRedo = list(tasksAchieved.curselection())
    if len(itemToRedo) == 0:
        showerror('Error', 'No task selected')
    else:
        index = itemToRedo[0]
        text = tasksAchieved.get(index)
        tasksAchieved.delete(index)
        tasksStarted.insert(END, text)

        conn_done = sqlite3.connect('Done.db')
        cursor_done = conn_done.cursor()

        conn = sqlite3.connect('Todo.db')
        cursor = conn.cursor()

        cursor_done.execute("DELETE FROM done WHERE item=?", (text,))
        conn_done.commit()

        cursor.execute("INSERT INTO todo (item) VALUES (?)", (text,))
        conn.commit()

        conn_done.close()
        conn.close()

def loadTasks():
    conn = sqlite3.connect('Todo.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT item FROM todo")
    rows = cursor.fetchall()

    tasksStarted.delete(0, END)
    
    for row in rows:
        tasksStarted.insert(END, row[0])
    
    conn.close()

def loadDoneTasks():
    conn_done = sqlite3.connect('Done.db')
    cursor_done = conn_done.cursor()

    cursor_done.execute("SELECT item FROM done")
    rows = cursor_done.fetchall()

    tasksAchieved.delete(0, END)

    for row in rows:
        tasksAchieved.insert(END, row[0])

    conn_done.close()

w,h,b,ft=994,700,'#FFF','Century Gothic'
 
global tasksStarted

TSCanv = Canvas(root, bg='#1AA4F6')
TACanv = Canvas(root, bg='#8aff70')
tasksStarted = Listbox(TSCanv, bd=2, relief='solid', width=25, height=15, font=(ft, 17, ''), highlightcolor='#0f0', selectmode=BROWSE)
tasksAchieved = Listbox(TACanv, bd=2, relief='solid', width=25, height=15, font=(ft, 17, ''), highlightcolor='#0f0', selectmode=BROWSE)

loadTasks()
loadDoneTasks()

scXS = Scrollbar(TSCanv, orient=HORIZONTAL, bg='#1AA4F6', command=tasksStarted.xview)
scXA = Scrollbar(TACanv, orient=HORIZONTAL, command=tasksAchieved.xview)
scYS = Scrollbar(TSCanv, orient=VERTICAL, command=tasksStarted.yview)
scYA = Scrollbar(TACanv, orient=VERTICAL, command=tasksAchieved.yview)

tasksStarted.configure(xscrollcommand=scXS.set, yscrollcommand=scYS.set)
tasksAchieved.configure(xscrollcommand=scXA.set, yscrollcommand=scYA.set)

scXS.pack(side=BOTTOM, fill=X)
scXA.pack(side=BOTTOM, fill=X)
scYS.pack(side=RIGHT, fill=Y)
scYA.pack(side=RIGHT, fill=Y)
tasksStarted.pack()
tasksAchieved.pack()
TSCanv.place(x=33, y=160)
TACanv.place(x=425, y=160)

scXS.pack(side=BOTTOM, fill=X)
scXA.pack(side=BOTTOM, fill=X)
scYS.pack(side=RIGHT, fill=Y)
scYA.pack(side=RIGHT, fill=Y)
tasksStarted.pack()
tasksAchieved.pack()
TSCanv.place(x=33, y=160)
TACanv.place(x=425, y=160)

scXS.pack(side=BOTTOM, fill=X)
scXA.pack(side=BOTTOM, fill=X)
scYS.pack(side=RIGHT, fill=Y)
scYA.pack(side=RIGHT, fill=Y)
tasksStarted.pack()
tasksAchieved.pack()
TSCanv.place(x=33, y=160)
TACanv.place(x=425, y=160)

def set_scrollregion(event=None):
    tasksStarted.configure(scrollregion=tasksStarted.bbox("all"))
    tasksAchieved.configure(scrollregion=tasksAchieved.bbox("all"))

def on_mousewheel(event):
    if event.delta > 0:
        tasksStarted.yview_scroll(-1, "units")
        tasksAchieved.yview_scroll(-1, "units")
    elif event.delta < 0:
        tasksStarted.yview_scroll(1, "units")
        tasksAchieved.yview_scroll(1, "units")

tasksStarted.bind("<Configure>", set_scrollregion)
tasksAchieved.bind("<Configure>", set_scrollregion)
tasksStarted.bind("<MouseWheel>", on_mousewheel)
tasksAchieved.bind("<MouseWheel>", on_mousewheel)


IAdd = PhotoImage(file='img/add.gif')
IEdit = PhotoImage(file='img/edit.gif')
IDelete = PhotoImage(file='img/delete.gif')
I2Delete = PhotoImage(file='img/Edelete.gif')
IClear = PhotoImage(file='img/clear.gif')
IRedo = PhotoImage(file='img/redo.gif')
IFinished = PhotoImage(file='img/check.gif')
ISave = PhotoImage(file= 'img/save.gif')
IOpen = PhotoImage(file='img/open.gif')

BDelete = Button(root,width=42,height=40,image=IDelete,bd=0,highlightthickness=0, command=DeleteTS)
bDelete = Button(root,width=41,height=40,image=IDelete,bd=0,highlightthickness=0, command=DeleteTA)
BClear = Button(root,width=42,height=55,image=IClear,bd=0,highlightthickness=0, command=ClearTS)
bClear = Button(root,width=42,height=55,image=IClear,bd=0,highlightthickness=0, command=ClearTA)
BAdd = Button(root,width=42,height=45,image=IAdd,command=lambda:AddFunc(''),bd=0,highlightthickness=0)
BFinished = Button(root,width=42,height=40,image=IFinished,bd=0,highlightthickness=0, command=Finish)
BRedo = Button(root,width=42,height=40,image=IRedo,bd=0,highlightthickness=0, command=Redo)
BEdit = Button(root,width=40,height=40,image=IEdit,bd=0,highlightthickness=0, command=Edit)

BClear.place(x=335,y=610)
bClear.place(x=720,y=610)
BAdd.place(x=32,y=105)
BEdit.place(x=188,y=108)
BDelete.place(x=104,y=108)
bDelete.place(x=425,y=110)
BFinished.place(x=335,y=107)
BRedo.place(x=262,y=107)

root.mainloop()


