from tkinter import *
import time

# fenetre graphique
root = Tk()
root.title("TaskVault")
root.resizable(False, False)
root.geometry("454x642")

# arriere plan
bg = PhotoImage(file="img/background.gif")
my_label = Label(root, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

# fonction du menu
def list():
    root.destroy()
    import todolist

def calcul():
    root.destroy()
    import calculator

def date():
    root.destroy()
    import mycalendar

def open_currency():
    root.destroy()
    import currency

def open_suggest_feature():
    root.destroy()
    import feature

def open_review():
    root.destroy()
    import rating

def settings():
    selected_option = StringVar(root)
    selected_option.set("") 

    options = ["Choose your currency", "Suggest a feature", "Review"]
    dropdown = OptionMenu(root, selected_option, *options)
    dropdown.place(x=344, y=90) 

    def handle_option(*args):
        option = selected_option.get()

        if option == "Choose your currency":
            open_currency()
        elif option == "Suggest a feature":
            open_suggest_feature()
        elif option == "Review":
            open_review()

    selected_option.trace("w", handle_option)

def numbers():
    root.destroy()
    import statistics

def convert():
    root.destroy()
    import converter

def money():
    root.destroy()
    import todo

# Bouttons calculatrice
f_calculator = PhotoImage(file='img/calculator.gif')
btt_calculator = Button(root, width=100, height=114, image=f_calculator, command=calcul)
btt_calculator.place(x=172, y=218)

# Bouttons calendrier
f_calendar = PhotoImage(file='img/Calendar icon.gif')
btt_calendar = Button(root, width=112, height=101, image=f_calendar, command=date)
btt_calendar.place(x=302, y=375)

# Bouttons covertisseur
f_convert = PhotoImage(file='img/converter.gif')
btt_convert = Button(root, width=112, height=101, image=f_convert, command=convert)
btt_convert.place(x=166, y=378)

# Bouttons organisateur d'argent
f_money = PhotoImage(file='img/money.gif')
btt_money = Button(root, width=114, height=115, image=f_money, command=money)
btt_money.place(x=30, y=372)

# Bouttons statistiques
f_statistics = PhotoImage(file='img/statistics.gif')
btt_statistics = Button(root, width=115, height=114, image=f_statistics, command=numbers)
btt_statistics.place(x=30, y=218)

# Bouttons to do list
f_todo = PhotoImage(file='img/todo.gif')
btt_todo = Button(root, width=114, height=114, image=f_todo, command=list)
btt_todo.place(x=302, y=222)

# Bouttons parametres
f_settings = PhotoImage(file='img/settings.gif')
btt_settings = Button(root, width=80, height=80, image=f_settings, command=settings)
btt_settings.place(x=344, y=10)

# horloge
clock_label = Label(root, font=('Open Sans Light', 23, 'bold'), bg='#C6C6C6')
clock_label.place(x=20, y=20, width=120)

def update_clock():
    current_time = time.strftime('%H:%M')
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock)

update_clock()

root.mainloop()
