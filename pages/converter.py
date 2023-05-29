from tkinter import *
import requests
from tkinter import messagebox
from PIL import Image, ImageTk

root = Tk()

variable1 = StringVar(root)
variable2 = StringVar(root)

variable1.set("currency")
variable2.set("currency")

currency_flags = {
    "AED": "img/flag_aed.gif",
    "AUD": "img/flag_aud.gif",
    "CAD": "img/flag_cad.gif",
    "CHF": "img/flag_chf.gif",
    "CNY": "img/flag_china.gif",
    "DKK": "img/flag_dkk.gif",
    "EGP": "img/flag_egp.gif",
    "EUR": "img/flag_eu.gif",
    "GBP": "img/flag_uk.gif",
    "INR": "img/flag_india.gif",
    "JPY": "img/flag_japan.gif",
    "KRW": "img/flag_krw.gif",
    "MAD": "img/flag_mad.gif",
    "SAR": "img/flag_sar.gif",
    "USD": "img/flag_usa.gif",
}

flag_images = {}
for currency_code, flag_path in currency_flags.items():
    flag_image = Image.open(flag_path)
    flag_image = flag_image.resize((30, 20), Image.ANTIALIAS)
    flag_images[currency_code] = ImageTk.PhotoImage(flag_image)

def real_time_currency_conversion():
    from_currency = variable1.get()
    to_currency = variable2.get()

    if from_currency == "currency" or to_currency == "currency":
        show_error_message("Please select currencies.")
        return

    if not amount1_field.get():
        show_error_message("Please enter an amount to convert.")
        return

    api_key = "0Z0UA6PGTM5E0RVZ"

    base_url = r"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"

    main_url = base_url + "&from_currency=" + from_currency + "&to_currency=" + to_currency + "&apikey=" + api_key

    req_ob = requests.get(main_url)

    result = req_ob.json()

    if "Realtime Currency Exchange Rate" in result and "5. Exchange Rate" in result["Realtime Currency Exchange Rate"]:

        exchange_rate = float(result["Realtime Currency Exchange Rate"]['5. Exchange Rate'])

        amount = float(amount1_field.get())

        new_amount = round(amount * exchange_rate, 3)

        amount2_field.config(state='normal')
        amount2_field.delete(0, END)
        amount2_field.insert(0, str(new_amount))
        amount2_field.config(state='readonly')
    else:
        show_error_message("Currency conversion data not available now.")

def show_error_message(message):
    messagebox.showerror("Error", message)

def clear_all():
    amount1_field.delete(0, END)
    amount2_field.config(state='normal')
    amount2_field.delete(0, END)
    amount2_field.config(state='readonly')

def validate_amount1_field(action_type, new_value):
    if action_type == '1': 
        try:
            float(new_value)
            return True
        except ValueError:
            return False
    return True

root.title("Currency Converter")
root.resizable(False, False)
root.geometry("361x642")

bg = PhotoImage(file="img/Currency converter.gif")
my_label = Label(root, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

validate_float = root.register(validate_amount1_field)
amount1_field = Entry(root, font=("Arial", 15), validate="key", validatecommand=(validate_float, '%d', '%P'))
amount2_field = Entry(root, font=("Arial", 15), fg="#FFFFFF", readonlybackground="#000B29", state='readonly')

amount1_field.place(x=69, y=420)
amount2_field.place(x=69, y=200)

currency_code_list = ["AED", "AUD", "CAD", "CHF", "CNY", "DKK", "EGP", "EUR", "GBP", "INR", "JPY", "KRW", "MAD", "SAR", "USD"]

currency_code_list.sort()

# Create the dropdown menus with flags
from_currency_option = OptionMenu(root, variable1, *currency_code_list)
from_currency_option.place(x=5, y=300)
from_currency_menu = from_currency_option.nametowidget(from_currency_option.menuname)
from_currency_menu.config(font=('Arial', 10))

for currency_code, flag_image in flag_images.items():
    from_currency_menu.entryconfig(currency_code, image=flag_image, compound=LEFT)

to_currency_option = OptionMenu(root, variable2, *currency_code_list)
to_currency_option.place(x=270, y=300)
to_currency_menu = to_currency_option.nametowidget(to_currency_option.menuname)
to_currency_menu.config(font=('Arial', 10))

for currency_code, flag_image in flag_images.items():
    to_currency_menu.entryconfig(currency_code, image=flag_image, compound=LEFT)

button1 = Button(root, text="Convert", font=("Arial", 20), command=real_time_currency_conversion)
button1.place(x=120, y=500)

button2 = Button(root, text="Clear", bg="#FFFFFF", command=clear_all)
button2.place(x=159, y=565)

root.mainloop()






