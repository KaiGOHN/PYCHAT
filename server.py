#!/usr/bin/env python
# coding: utf-8

import socket
import threading
from server_functions import *
check_cfg()
class ClientThread(threading.Thread):
    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def run(self):
        print("Connection de %s %s" % (self.ip, self.port,))
        r = self.clientsocket.recv(2048)
        msg_recu = r.decode()
        print("Reçu {}".format(msg_recu))
        userinput = msg_recu.rsplit('"-"')
        print(userinput)
        command = (str(userinput[0]))[1:]
        if command == "login":
            login(userinput, self)
            print("Client déconnecté...")
        if command == "register":
            register(userinput, self)
            print("Client déconnecté...")





tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((readcfg(['SOCKET','host']), int(readcfg(['SOCKET','port']))))

while True:
    tcpsock.listen(10)
    print("En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()