from gui_chat import *
from gui_register import *


def callback(event):
    gui_register()

def gui_login():
    def loginbutton():
        username = str(entree_username.get())
        password = str(entree_password.get())
        log = login(username, password)
        if log == True:
            fenetre.destroy()
            gui_chat()
        elif log == "err1":
            showwarning('ERR1', 'SERVEUR INACESSIBLE')
        elif log == "err3":
            showwarning('ERR3', 'BASE DE DONNÉE INACESSIBLE')
        else:
            showwarning("ERR2", "NOM D'UTILISATEUR OU MOT DE PASSE INVALIDE")
            username_entry.set('')
            password_entry.set('')

    fenetre = Tk()
    fenetre.resizable(width=FALSE, height=FALSE)
    fenetre.title("Log-In")
    fenetre.geometry("200x150")

    username_entry = StringVar()
    password_entry = StringVar()

    username_text = Label(fenetre, text="Nom d'utilisateur:")
    entree_username = Entry(fenetre, textvariable=username_entry, width=30)

    password_text = Label(fenetre, text="Mot de passe:")
    entree_password = Entry(fenetre, textvariable=password_entry, show="*", width=30)

    bouton = Button(fenetre, text="Se connecter", command=loginbutton)

    link = Label(fenetre, text="S'inscrire", fg="blue", cursor="hand2")

    username_text.pack()
    entree_username.pack()
    password_text.pack()
    entree_password.pack()
    bouton.pack()
    link.pack()

    link.bind("<Button-1>", callback)

    fenetre.mainloop()
