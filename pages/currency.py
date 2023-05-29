import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

def submit():
    selected_currency = currency_variable.get()
    selected_symbol = currency_symbols[selected_currency]
    messagebox.showinfo("Currency Selection", "Selected Currency: {}\nSelected Symbol: {}".format(selected_currency, selected_symbol))
    
    conn = sqlite3.connect('currency.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS currency
                      (id INTEGER PRIMARY KEY, code TEXT, symbol TEXT)''')
    
    cursor.execute("DELETE FROM currency")
    
    cursor.execute("INSERT INTO currency (code, symbol) VALUES (?, ?)", (selected_currency, selected_symbol))
    
    conn.commit()
    conn.close()

window = tk.Tk()
window.title("Currency Selection")
window.geometry("300x300")
window.resizable(False, False)

currency_flags = {
    "AED": {"flag": "img/flag_aed.gif", "symbol": "د.إ"},
    "AUD": {"flag": "img/flag_aud.gif", "symbol": "$"},
    "CAD": {"flag": "img/flag_cad.gif", "symbol": "$"},
    "CHF": {"flag": "img/flag_chf.gif", "symbol": "Fr"},
    "CNY": {"flag": "img/flag_china.gif", "symbol": "¥"},
    "DKK": {"flag": "img/flag_dkk.gif", "symbol": "kr"},
    "EGP": {"flag": "img/flag_egp.gif", "symbol": "£"},
    "EUR": {"flag": "img/flag_eu.gif", "symbol": "€"},
    "GBP": {"flag": "img/flag_uk.gif", "symbol": "£"},
    "INR": {"flag": "img/flag_india.gif", "symbol": "₹"},
    "JPY": {"flag": "img/flag_japan.gif", "symbol": "¥"},
    "KRW": {"flag": "img/flag_krw.gif", "symbol": "₩"},
    "MAD": {"flag": "img/flag_mad.gif", "symbol": "د.م."},
    "SAR": {"flag": "img/flag_sar.gif", "symbol": "﷼"},
    "USD": {"flag": "img/flag_usa.gif", "symbol": "$"},
}

currency_variable = StringVar(window)

sorted_currency_codes = sorted(currency_flags.keys())

currency_dropdown = OptionMenu(window, currency_variable, *sorted_currency_codes)
currency_dropdown.pack(pady=20)

currency_variable.set("EUR")

flag_images = {}
currency_symbols = {}
for currency_code, currency_info in currency_flags.items():
    flag_path = currency_info["flag"]
    flag_image = Image.open(flag_path)
    flag_image = flag_image.resize((30, 20), Image.ANTIALIAS)
    flag_images[currency_code] = ImageTk.PhotoImage(flag_image)
    currency_symbols[currency_code] = currency_info["symbol"]

menu = currency_dropdown.nametowidget(currency_dropdown.menuname)
menu.config(font=('Arial', 10)) 

for currency_code, flag_image in flag_images.items():
    menu.entryconfig(currency_code, image=flag_image, compound=LEFT)

conn = sqlite3.connect('currency.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS currency
                  (id INTEGER PRIMARY KEY, code TEXT, symbol TEXT)''')

cursor.execute("SELECT * FROM currency")
rows = cursor.fetchall()
if len(rows) == 0:
    default_currency_code = "EUR"
    default_currency_symbol = currency_symbols[default_currency_code]
    cursor.execute("INSERT INTO currency (code, symbol) VALUES (?, ?)", (default_currency_code, default_currency_symbol))

conn.commit()
conn.close()

submit_button = Button(window, text="Submit", command=submit)
submit_button.pack(pady=10)

window.mainloop()
