from tkinter import *
from tkinter import messagebox

expression = ""

def appuyer(touche):
    if touche == "=":
        calculer()
        return
   
    global expression
    expression += str(touche)
    equation.set(expression)


def calculer():
    try:
        global expression
        total = str(eval(expression))
        equation.set(total)
        expression = total
    except:
        equation.set("erreur")
        expression=""


def effacer():
    global expression
    expression = ""
    equation.set("")


if __name__ == "__main__":
    root = Tk()
    root.title("Calculatrice")
    root.resizable(False, False)
    root.geometry("453x642")

    # Calculate the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    
    window_width = 453
    window_height = 642
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.update_idletasks()

    bg = PhotoImage(file="img/calcul.gif")
    my_label = Label(root, image=bg)
    my_label.place(x=0, y=0, relwidth=1, relheight=1)

    equation = StringVar()

    
    result_label_width = 300
    result_label_height = 80
    result_label_x = (window_width - result_label_width) // 2
    result_label_y = 50

    resultat = Label(root, bg="#101419", fg="#FFF", textvariable=equation, height=2, width=16, font=("Arial", 20))
    resultat.place(x=result_label_x, y=result_label_y, width=result_label_width, height=result_label_height)

    boutons = [7, 8, 9, "*", 4, 5, 6, "-", 1, 2, 3, "+", 0, ".", "/", "="]
    ligne = 1
    colonne = 0

    button_width = 75
    button_height = 80
    button_spacing_x = 15
    button_spacing_y = 10
    button_start_x = (window_width - (button_width * 4 + button_spacing_x * 3)) // 2
    button_start_y = result_label_y + result_label_height + button_spacing_y

    for bouton in boutons:
        b = Label(root, text=str(bouton), bg="#476C9B", fg="#FFF", height=3, width=5, font=("Arial", 14))
        b.place(x=button_start_x + colonne * (button_width + button_spacing_x), y=button_start_y + ligne * (button_height + button_spacing_y), width=button_width, height=button_height)
        # Rendre le texte cliquable
        b.bind("<Button-1>", lambda e, bouton=bouton: appuyer(bouton))

        colonne += 1
        if colonne == 4:
            colonne = 0
            ligne += 1
   
    
    delete_button_width = 300
    delete_button_height = 40
    delete_button_x = (window_width - delete_button_width) // 2
    delete_button_y = button_start_y + 5 * (button_height + button_spacing_y) + button_spacing_y

    # Bouton pour effacer
    b = Label(root, text="Effacer", bg="#984447", fg="#FFF", height=3, width=20, font=("Arial", 12))
    b.place(x=delete_button_x, y=delete_button_y, width=delete_button_width, height=delete_button_height)
    b.bind("<Button-1>", lambda e: effacer())

    # Demarrer l'interface graphique
    root.mainloop()
