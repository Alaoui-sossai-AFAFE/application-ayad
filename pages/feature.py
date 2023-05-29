import tkinter as tk
from tkinter import messagebox

def submit():
    suggestion = entry.get("1.0", "end-1c")
    if suggestion:
        messagebox.showinfo("Thank You", "Thank you! Your feature will be taken into consideration.")
        window.destroy()
    else:
        messagebox.showerror("Error", "Please enter a feature suggestion.")

window = tk.Tk()
window.title("Feature Suggestion")
window.resizable(False, False)
window.geometry("300x300")

bg = tk.PhotoImage(file="img/feature.gif")
my_label = tk.Label(window, image=bg)
my_label.image = bg
my_label.place(x=0, y=0, relwidth=1, relheight=1)

entry = tk.Text(window, width=30, height=10)
entry.place(x=26, y=68)

submit_button = tk.Button(window, text="Submit", command=submit)
submit_button.place(x=120, y=250)

window.mainloop()