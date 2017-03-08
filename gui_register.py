from tkinter import *
from client_functions import *
from tkinter.messagebox import *
from re import *

def gui_register():
    def resgisterbutton():
        username = str(entree_username.get())
        password = str(entree_password.get())
        first_name = str(entree_first_name.get())
        last_name = str(entree_last_name.get())
        email = str(entree_email.get())
        if len(password) <= 16 and len(password) >= 8:
            password_test = True
        else:
            password_test = False
        email_regex = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)
        if email_regex is not None and password_test == True:
            log = register(username, password, first_name, last_name, email)
            if log == True:
                registerwindow.destroy()
            elif log == "err1":
                showwarning('ERR1', 'SERVEUR INACESSIBLE')
            elif log == "err3":
                showwarning('ERR3', 'BASE DE DONNÉE INACESSIBLE')
            elif log == "err4":
                showwarning('ERR4', "NOM D'UTILISATEUR OU EMAIL NON DISPONIBLE")
        else:
            showwarning('ERREUR', 'EMAIL OU MOT DE PASSE INVALIDE')
    registerwindow = Tk()
    registerwindow.title("Inscription")

    username_entry = StringVar()
    password_entry = StringVar()
    first_name_entry = StringVar()
    last_name_entry = StringVar()
    email_entry = StringVar()

    username_text = Label(registerwindow, text="Nom d'utilisateur:")
    entree_username = Entry(registerwindow, textvariable=username_entry, width=50)

    password_text = Label(registerwindow, text="Mot de passe:")
    entree_password = Entry(registerwindow, textvariable=password_entry, show="*", width=50)

    first_name_text = Label(registerwindow, text="Prénom:")
    entree_first_name = Entry(registerwindow, textvariable=first_name_entry, show="", width=50)

    last_name_text = Label(registerwindow, text="Nom de famille:")
    entree_last_name = Entry(registerwindow, textvariable=last_name_entry, show="", width=50)

    email_text = Label(registerwindow, text="email:")
    entree_email = Entry(registerwindow, textvariable=email_entry, show="", width=50)

    bouton = Button(registerwindow, text="S'inscrire", command=resgisterbutton)

    username_text.pack()
    entree_username.pack()
    password_text.pack()
    entree_password.pack()
    first_name_text.pack()
    entree_first_name.pack()
    last_name_text.pack()
    entree_last_name.pack()
    email_text.pack()
    entree_email.pack()
    bouton.pack()
    registerwindow.mainloop()
