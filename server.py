#!/usr/bin/env python
# coding: utf-8

import socket
import threading

from server_functions import *

check_cfg()
global clientslist
clientslist = []
class ClientThread(threading.Thread):
    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        # print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))
        global clientslist
        clientslist.append(clientsocket)


    def run(self):
        global clientslist
        # print("Connection de %s %s" % (self.ip, self.port,))
        r = self.clientsocket.recv(1024)
        msg_recu = pickle.loads(r)
        # print("Reçu {}".format(msg_recu))
        command = str(msg_recu[0])
        if command == "login":
            login(msg_recu, self)
        if command == "register":
            register(msg_recu, self)
        if command == "sendmsg":
            sendmsg(msg_recu, self)
        if command == "loadlastid":
            loadlastid(self)
        if command == "get_msg":
            get_msg(msg_recu, self)






tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((readcfg(['SOCKET','host']), int(readcfg(['SOCKET','port']))))

while True:
    tcpsock.listen(10)
    # print("En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()