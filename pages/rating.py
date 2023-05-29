import tkinter as tk
from tkinter import *
from tkinter import messagebox

review = tk.Tk()
review.transient(review.master)
review.resizable(False, False)
review.title("Review")
review.geometry("300x300")

bg = PhotoImage(file="img/white.gif")
my_label = Label(review, image=bg)
my_label.image = bg
my_label.place(x=0, y=0, relwidth=1, relheight=1)

frame = Frame(review)
frame.pack(side=TOP, anchor=CENTER)

star_labels = []
selected_stars = 0

def toggle_star(index):
    global selected_stars

    if selected_stars == index + 1:
        selected_stars -= 1
    else:
        selected_stars = index + 1

    update_stars()

def update_stars():
    full_star = '\u2605'
    empty_star = '\u2606'

    for i, star_label in enumerate(star_labels):
        if i < selected_stars:
            star_label.config(text=full_star)
        else:
            star_label.config(text=empty_star)

full_star = '\u2605'
empty_star = '\u2606'

for i in range(5):
    star_label = Label(frame, text=empty_star, font=('Arial', 24))
    star_label.pack(side=LEFT, padx=2)
    star_label.bind('<Button-1>', lambda e, index=i: toggle_star(index))
    star_labels.append(star_label)

update_stars()

review_label = Label(review, text="Write your review:", font=('Arial', 12))
review_label.pack(side=TOP, pady=10)

entry = Text(review, width=30, height=10)
entry.pack(side=TOP)

def submit():
    review_text = entry.get("1.0", END).strip()
    if review_text:
        messagebox.showinfo("Thank You", "Thank you for your review!")
        review.destroy()
    else:
        messagebox.showerror("Error", "Please write a review before submitting.")

submit_button = Button(review, text="Submit", command=submit)
submit_button.pack(side=TOP, pady=10)

review.mainloop()
