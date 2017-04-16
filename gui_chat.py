import time
from threading import Thread
from tkinter import *

from client_functions import *


def close():
    global Running
    Running = False


def gui_chat(a):
    global username
    username = a
    global launch
    launch = 1
    global Running
    Running = True
    global guichat
    guichat = Tk()
    guichat.title("Chat")
    guichat.title('PYCHAT')
    guichat.geometry("800x450")
    guichat.resizable(width=FALSE, height=FALSE)
    global chat
    chat = Text(guichat, bd=0, bg="white", height="7", width="770", font="Arial")
    chat.config(state=DISABLED)
    scrollbar = Scrollbar(guichat, command=chat.yview)
    chat['yscrollcommand'] = scrollbar.set
    Button1 = Button(guichat, text="Send", width="12", height="5", command=send)
    global Entry1
    global Message
    Message = StringVar()
    Entry1 = Entry(guichat, textvariable=Message, bg='bisque', fg='maroon')
    scrollbar.place(x=780, y=0, height=390)
    chat.place(x=5, y=5, height=390, width=770)
    Entry1.place(x=5, y=410, height=30, width=650)
    Button1.place(x=680, y=410, height=30)
    thread_1 = RefreshMessages()
    thread_1.start()
    guichat.mainloop()
    close()


def send():
    msg = str(Entry1.get())
    sendmsg(username, msg)
    Message.set('')


class RefreshMessages(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        localidlist = []
        while Running == True:
            try:
                time.sleep(1)
                global guichat
                # request = requests.get("http://"+ readcfg(['HTTP', 'host'])+ ":" + readcfg(['HTTP', 'port']) + "/idlist.txt")
                # request = request.text
                # idlist = request.split("\r\n")
                # idlist = idlist[:-1]
                idlist = loadidslist(username)
                for item in idlist:
                    item = str(item)[1:-2]
                    if (item not in localidlist) is True:
                        data = get_msg(item)
                        localidlist.append(item)
                        text = "[" + str(data[3]) + "] " + "<" + str(data[1]) + "> " + str(data[2]) + "\n"
                        chat.config(state=NORMAL)
                        chat.insert(END, text)
                        chat.config(state=DISABLED)
            except:
                pass