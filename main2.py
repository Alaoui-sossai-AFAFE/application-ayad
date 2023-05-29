from tkinter import *      # * signifie tout
from tkinter.messagebox import *
from tkinter.filedialog import *
import pickle
app = Tk()
app.title('TO DO')
app.geometry('994x700')
app.resizable(width=False, height=True)
app.config(background='#FFF')
global taskStarted 
# TSCanvas = Canvas(app)
# TACanvas = Canvas(app)
# TSscrollX = Scrollbar(TSCanvas, orient=HORIZONTAL)
# TAscrollX = Scrollbar(TACanvas, orient=HORIZONTAL)
# TSscrollY = Scrollbar(TSCanvas, orient=VERTICAL)
# TAscrollY = Scrollbar(TACanvas, orient=VERTICAL)
# ft = 'Century Gothic'
# taskStarted = Listbox(TSCanvas,
#     bd=2,
#     relief='solid',
#     width=38,
#     height=19,
#     font=(ft,16,''),
#     xscrollcommand=TSscrollX.set,
#     yscrollcommand=TSscrollY.set,
#     selectmode=BROWSE
# )
# taskAchieve = Listbox(TACanvas,
#     bd=2,
#     relief='solid',
#     width=38,
#     height=19,
#     font=(ft,16,''),
#     xscrollcommand=TAscrollX.set,
#     yscrollcommand=TAscrollY.set,
#     selectmode=BROWSE
# )

# b = '#FFF'
# labelTS = Label(app,
#     text='Task Started',
#     bg=b,
#     fg='#FFF',
#     font=(ft,25,'bold')
#     )
# labelTA = Label(app,
#     text='Task Achieved',
#     bg=b,
#     fg='#FFF',
#     font=(ft,25,'bold')
#     )
# app.mainloop()

# ---------------------- Les modules utilisés
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import pickle
# ---------------------- Les fonctions qui sont utilisées par le programme
def AddFunc(txt,index=END):
    global add
    add = Tk()
    add.title('Add Note')
    add.geometry('800x600')
    add.resizable(width=False, height=False)
    add.config(background='#FFF')
    global Write 
    Write = Text(add,font=(ft,16,''))
    Write.insert(END, txt)
    Write.pack()
    w,h = 7,1
    bConfirm = Button(add,
        text='Confirm',
        width=w,height=h,bd=0,highlightthickness=0,
        font=(ft,20), fg='#FFF',
        bg='#00a32e', command=lambda:GetText(index))
    bConfirm.place(x=670, y=530)
    add.mainloop()
def GetText(index=END):
    text = Write.get('1.0' ,END)
    tasksStarted.insert(index,text)
    add.destroy()

def Save(none=0):
    pass
def Edit():
    itemToEdit = list(tasksStarted.size())[itemToEdit[0]]
    if(len(itemToEdit) == 0):
        texte = tasksStarted.get(0, tasksStarted.size())[itemToEdit[0]]
        tasksStarted.delete(itemToEdit[0])
        AddFunc(texte,itemToEdit)
    else:
        showerror('Error','No task sekected')

def Delete():
    itemTode1 = list(tasksStarted.curselection())
    if(len(itemTode1) == 0):
        showerror('Error','You must select at least one task')
    else:
        tasksStarted.delete(itemTode1[0])
def Clear():
    TSsize = tasksStarted.size()
    TAsize = tasksAchieved.size()
    if(TSsize > 0 or TAsize):
        yesNo = askyesno('Warning', 'Are you sure you want to clear all tasks')
        if (yesNo == True):
            tasksStarted.delete(0,END)
            tasksAchieved.delete(0,END)
        else:
            showwarning('Warning','Taks are already clear')
def Finish():
    itemToFinish = list(tasksStarted.curselection())
    if(len(itemToFinish) != 0):
        textToFinish = tasksStarted.get(itemToFinish)
        tasksAchieved.insert(END, textToFinish)
        tasksStarted.delete(itemToFinish)
    else:
        showerror('Error','You should select a task')
def Redo():
    pass
    

    # ---------------------- Importantes variables
# Ici on déclare 4 variables (En utilisant une ligne) la largeur et la longeur, la couleur blanche et le nom de la police du texte
w,h,b,ft=994,700,'#FFF','Century Gothic'  # Declaration des variables, largeur, hauteur, couleur, police d ecriture
# ---------------------- Paramètres de la fenêtre
app = Tk()#declarer la fenetre principale
# L'icone de la fenetre principale
app.iconbitmap('imgf/icon.ico')
# Le titre
app.title('TO DO LIST') 
# La taille (ou la résolution)
app.geometry(f'{w}x{h}')#les dimenssions w et h st definies ci-haut
# la désactivation de changement de la résolution de fenêtre
app.resizable(width=False,height=False)
# la couleur de l'arrière plan (background)
app.config(background='#FFF')
# ---------------------- Paramètres du menu (dans le haut de la fenêtre)
MenuApp = Menu(app)
app.config(menu=MenuApp)
mFile = Menu(MenuApp)
# Les grands titres du menu
MenuApp.add_cascade(label='File',menu=mFile)
# Les sous-titres du menu
mFile.add_command(label='Save',accelerator='(Ctrl+S)')#il faut ajouter la :command = ...
# ---------------------- Paramètres des widgets
# Déclaration d'une variable *global*
global tasksStarted
# Déclaration de plusieurs widgets, ex: des canvas, des barres de défilement, des listes et des textes
TSCanv = Canvas(app,bg='#1AA4F6')#COULEUR
TACanv = Canvas(app,bg='#8aff70')
scXS = Scrollbar(TSCanv,orient=HORIZONTAL,bg='#1AA4F6')
scXA = Scrollbar(TACanv,orient=HORIZONTAL)
scYS = Scrollbar(TSCanv,orient=VERTICAL)
scYA = Scrollbar(TACanv,orient=VERTICAL)
tasksStarted = Listbox(TSCanv,bd=2,relief='solid',width=38,height=19,font=(ft,16,''),highlightcolor='#0f0',xscrollcommand=scXS.set,yscrollcommand=scYS.set,selectmode=BROWSE)
tasksAchieved = Listbox(TACanv,bd=2,relief='solid',width=38,height=19,font=(ft,16,''),highlightcolor='#0f0',xscrollcommand=scXA.set,yscrollcommand=scYA.set,selectmode=BROWSE)
labeltS = Label(app,text='Tasks Started :',bg=b,fg='#F00',font=(ft,25,'bold'))
labeltA = Label(app,text='Tasks Achieved :',bg=b,fg='#F00',font=(ft,25,'bold'))
# Positionnement des widgets
scXS.pack(side=BOTTOM,fill=X)# https://www.tutorialspoint.com/python/tk_pack.htm
scXA.pack(side=BOTTOM,fill=X)
scYS.pack(side=RIGHT,fill=Y)
scYA.pack(side=RIGHT,fill=Y)
tasksStarted.pack()
tasksAchieved.pack()
scXS.config(command=tasksStarted.xview)
scXA.config(command=tasksStarted.xview)
scYS.config(command=tasksStarted.yview)
scYA.config(command=tasksStarted.yview)
TSCanv.place(x=10,y=60)
TACanv.place(x=505,y=60)
labeltS.place(x=50,y=10)
labeltA.place(x=540,y=10)

# ---------------------- les raccourcis claviers
app.bind('<Control_L><s>')#il faut ajouter la commande
# ---------------------- Les images des bouttons
IAdd = PhotoImage(file='imgf2/Add.gif')
#pour inserer des images en png,jpg, ou autres, utiliser:
#IAdd = ImageTk.PhotoImage(Image.open('img/Add.png'))

IEdit = PhotoImage(file='imgf2/Edit.gif')
IDelete = PhotoImage(file='imgf2/Delete.gif')
IClear = PhotoImage(file='imgf2/ClearD.gif')
IDAdd = PhotoImage(file='imgf2/AddD.gif')
IDEdit = PhotoImage(file='imgf2/EditD.gif')
IDDelete = PhotoImage(file='imgf2/DeleteD.gif')
IDClear = PhotoImage(file='imgf2/ClearD.gif')
iAdd = PhotoImage(file='imgf2/plus.gif')
iEdit = PhotoImage(file='imgf2/pencil.gif')
iDelete = PhotoImage(file='imgf2/minus.gif')
iRedo = PhotoImage(file='imgf2/redo.gif')
iFinished = PhotoImage(file='imgf2/finished.gif')
idAdd = PhotoImage(file='imgf2/plusD.gif')
idEdit = PhotoImage(file='imgf2/pencilD.gif')
idDelete = PhotoImage(file='imgf2/minusD.gif')
idRedo = PhotoImage(file='imgf2/redoD.gif')
idFinished = PhotoImage(file='imgf2/finishedD.gif')

# ---------------------- Les bouttons
# Déclaration de 4 variables (dans une ligne) des tailles des grands et petits bouttons
Wd,Hg,wd,hg=165,56,40,40
BAdd = Button(app,text='Add',width=Wd,height=Hg,image=IAdd,command=lambda:AddFunc(''),bd=0,highlightthickness=0)
BEdit = Button(app,text='Edit',width=Wd,height=Hg,image=IEdit,bd=0,highlightthickness=0, command=Edit)
BDelete = Button(app,text='Delete',width=Wd,height=Hg,image=IDelete,bd=0,highlightthickness=0, command=Delete)
BClear = Button(app,text='Clear',width=Wd,height=Hg,image=IClear,bd=0,highlightthickness=0, command=Clear)
bAdd = Button(app,text='+',width=wd,height=hg,image=iAdd,command=lambda:AddFunc(''),bd=0,highlightthickness=0)
bDelete = Button(app,text='-',width=wd,height=hg,image=iDelete,bd=0,highlightthickness=0, command=Delete)
bFinished = Button(app,text='E',width=wd,height=hg,image=iFinished,bd=0,highlightthickness=0, command=Finish)
bRedo = Button(app,text='<-',width=wd,height=hg,image=iRedo,bd=0,highlightthickness=0, command=Redo)
bEdit = Button(app,text='<-',width=wd,height=hg,image=iEdit,bd=0,highlightthickness=0, command=Redo)
# Positionnement des boutons 
BClear.place(x=820,y=580)
bAdd.place(x=350,y=12)
bDelete.place(x=400,y=12)
BEdit.place(x=270,y=580)
BAdd.place(x=10,y=580)
BDelete.place(x=570,y=580)
bFinished.place(x=450,y=12)
bRedo.place(x=895,y=12)
bEdit.place(x=945,y=12)
# ---------------------- Ouverture du programme
app.mainloop()