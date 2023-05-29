import matplotlib.pyplot as plt
from matplotlib.image import imread
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import sqlite3

# Create the main window
main_window = tk.Tk()
main_window.title("Dashboard")
main_window.resizable(False, False)

# Load the background and graph images
background_image = imread('img/Dashboard.gif')
bg_image = imread('img/back.gif')

# Create the figure and axes
fig_bg = plt.figure(figsize=(6.3, 6.3), dpi=100)
ax_bg = fig_bg.add_axes([0, 0, 1, 1])
ax_bg.imshow(background_image)
ax_bg.axis('off')

fig_graph = plt.figure(1, figsize=(6.3, 6.3), dpi=100)
ax_graph = fig_graph.add_subplot(111)

# Fetch data from the database
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()
cursor.execute("SELECT option, SUM(price) FROM expenses GROUP BY option")
data = cursor.fetchall()
conn.close()

# Extract options and prices from the data
options = [row[0] for row in data]
prices = [row[1] for row in data]

# Set the axis limits
x_start = -0.5
x_end = len(options) - 0.5
y_start = 0
y_end = max(prices)

bar_colors = ['#7950F2', '#12B886', '#C30147', '#737373', '#228BE6', 'orange']

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

ax_graph.imshow(bg_image, extent=[x_start, x_end, y_start, y_end], aspect='auto')
bars = ax_graph.bar(range(len(options)), prices, color=bar_colors)
ax_graph.set_ylabel('Total Expense')
ax_graph.set_xticks([])

for i, bar in enumerate(bars):
    height = bar.get_height()
    label = f"{prices[i]} {currency_symbol}"
    ax_graph.text(bar.get_x() + bar.get_width() / 2, height, label, ha='center', va='bottom')

canvas = FigureCanvasTkAgg(fig_graph, master=main_window)
canvas.draw()
canvas.get_tk_widget().pack()

main_window.mainloop()
