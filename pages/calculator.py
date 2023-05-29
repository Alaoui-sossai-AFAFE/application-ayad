import tkinter as tk

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"

window = tk.Tk()
window.geometry("375x667")
window.resizable(0, 0)
window.title("Calculator")

total_expression = ""
current_expression = ""

display_frame = tk.Frame(window, height=221, bg=LIGHT_GRAY)
display_frame.pack(expand=True, fill="both")

total_label = tk.Label(display_frame, text=total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                       fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
total_label.pack(expand=True, fill='both')

label = tk.Label(display_frame, text=current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                 fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
label.pack(expand=True, fill='both')

digits = {
    7: (1, 1), 8: (1, 2), 9: (1, 3),
    4: (2, 1), 5: (2, 2), 6: (2, 3),
    1: (3, 1), 2: (3, 2), 3: (3, 3),
    0: (4, 2), '.': (4, 1)
}
operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

buttons_frame = tk.Frame(window)
buttons_frame.pack(expand=True, fill="both")

buttons_frame.rowconfigure(0, weight=1)
for x in range(1, 5):
    buttons_frame.rowconfigure(x, weight=1)
    buttons_frame.columnconfigure(x, weight=1)


def add_to_expression(value):
    global current_expression
    current_expression += str(value)
    update_label()


def create_digit_buttons():
    for digit, grid_value in digits.items():
        button = tk.Button(buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                           borderwidth=0, command=lambda x=digit: add_to_expression(x))
        button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)


def append_operator(operator):
    global current_expression, total_expression
    current_expression += operator
    total_expression += current_expression
    current_expression = ""
    update_total_label()
    update_label()


def create_operator_buttons():
    i = 0
    for operator, symbol in operations.items():
        button = tk.Button(buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=lambda x=operator: append_operator(x))
        button.grid(row=i, column=4, sticky=tk.NSEW)
        i += 1


def clear():
    global current_expression, total_expression
    current_expression = ""
    total_expression = ""
    update_label()
    update_total_label()


def create_clear_button():
    button = tk.Button(buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                       borderwidth=0, command=clear)
    button.grid(row=0, column=1, sticky=tk.NSEW)


def square():
    global current_expression
    current_expression = str(eval(f"{current_expression}**2"))
    update_label()

def create_square_button():
    button = tk.Button(buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
    borderwidth=0, command=square)
    button.grid(row=0, column=2, sticky=tk.NSEW)

def sqrt():
    global current_expression
    current_expression = str(eval(f"{current_expression}**0.5"))
    update_label()

def create_sqrt_button():
    button = tk.Button(buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
    borderwidth=0, command=sqrt)
    button.grid(row=0, column=3, sticky=tk.NSEW)

def evaluate():
    global current_expression, total_expression
    total_expression += current_expression
    update_total_label()
    try:
        current_expression = str(eval(total_expression))
        total_expression = ""
    except Exception as e:
        current_expression = "Error"
    finally:
        update_label()

def create_equals_button():
    button = tk.Button(buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
    borderwidth=0, command=evaluate)
    button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

def create_buttons_frame():
    frame = tk.Frame(window)
    frame.pack(expand=True, fill="both")
    return frame

def update_total_label():
    expression = total_expression
    for operator, symbol in operations.items():
        expression = expression.replace(operator, f' {symbol} ')
        total_label.config(text=expression)

def update_label():
    label.config(text=current_expression[:11])

def run():
    window.mainloop()

create_digit_buttons()
create_operator_buttons()
create_clear_button()
create_equals_button()
create_square_button()
create_sqrt_button()
run()