import calendar
import tkinter as tk

def toggle_checkbox(row, col):
    checkboxes[row][col].toggle()

def create_checkbox(row, col):
    checkbox_frame = tk.Frame(root)
    checkbox_frame.grid(row=row+2, column=col+1, sticky='nsew')

    checkbox = tk.Checkbutton(checkbox_frame)
    checkbox.pack(side='left')

    separator = tk.Frame(checkbox_frame, height=2, relief='flat')  
    separator.pack(fill='x')

    return checkbox

def create_label(text, row, col):
    label = tk.Label(root, text=text, padx=10, pady=5)
    label.grid(row=row+2, column=col, sticky='nsew')
    separator = tk.Frame(root, height=2, relief='groove')
    separator.grid(row=row+3, column=col, sticky='ew')
    return label

def add_habit():
    habit_title = entry.get()
    if habit_title:
        habit_titles.append(habit_title)
        create_label(habit_title, 0, len(habit_titles))
        for i in range(len(days_of_week)):
            checkboxes[i].append(create_checkbox(i+1, len(habit_titles)-1))
        if first_day_index > 0:
            checkboxes[0][len(habit_titles)-1].grid(row=first_day_index+2, column=len(habit_titles))
        if first_day_index < 6:
            checkboxes[6][len(habit_titles)-1].grid(row=1, column=len(habit_titles))
        entry.delete(0, tk.END)
        checkboxes_frame.update()

root = tk.Tk()
root.title('Habit Tracker')

days_of_week = list(calendar.day_name)

first_day_index = days_of_week.index('Monday')

days_of_week = days_of_week[first_day_index:] + days_of_week[:first_day_index]

habit_titles = []

for i, day in enumerate(days_of_week):
    create_label(day, i, 0)

checkboxes_frame = tk.Frame(root) 
checkboxes_frame.grid(row=2, column=1, rowspan=len(days_of_week), sticky='nsew')

checkboxes = [[create_checkbox(row, col) for col in range(len(habit_titles))] for row in range(len(days_of_week))]

entry = tk.Entry(root)
entry.grid(row=len(days_of_week)+2, column=0, columnspan=2, pady=10)

add_button = tk.Button(root, text='Add Habit', command=add_habit)
add_button.grid(row=len(days_of_week)+3, column=0, columnspan=2)

root.mainloop()
