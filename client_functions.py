#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import os.path
import pickle
import socket


def readcfg(list):
    config = configparser.ConfigParser()
    config.read('client_config.ini')
    for item in list:
        config = config[item]
    return str(config)


def connect(host, port):
    try :
        connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion_avec_serveur.connect((host, int(port)))
        return connexion_avec_serveur
    except:
        return "err1"


def send(msg_a_envoyer,connexion_avec_serveur ):
    msg_a_envoyer = pickle.dumps(msg_a_envoyer)
    connexion_avec_serveur.send(msg_a_envoyer)

def recv(connexion_avec_serveur):
    msg_recu = connexion_avec_serveur.recv(1024)
    stringdata = pickle.loads(msg_recu)
    return stringdata

def disconnect(connexion_avec_serveur):
    connexion_avec_serveur.shutdown(1)
    connexion_avec_serveur.close()

def login(username, password):
    connexion_avec_serveur = connect(readcfg(['SOCKET','host']), readcfg(['SOCKET','port']))
    if connexion_avec_serveur == "err1":
        return "err1"
    else:
        msg_a_envoyer = ["login", username, password]
        send(msg_a_envoyer,connexion_avec_serveur)
        stringdata = recv(connexion_avec_serveur)
        disconnect(connexion_avec_serveur)
        if stringdata == "logs ok":
            return True
        else:
            return stringdata


def sendmsg(username, msg):
    connexion_avec_serveur = connect(readcfg(['SOCKET', 'host']), readcfg(['SOCKET', 'port']))
    if connexion_avec_serveur == "err1":
        return "err1"
    else:
        msg_a_envoyer = ["sendmsg", username, msg]
        send(msg_a_envoyer, connexion_avec_serveur)


def loadidslist(username):
    connexion_avec_serveur = connect(readcfg(['SOCKET', 'host']), readcfg(['SOCKET', 'port']))
    msg_a_envoyer = ["loadidslist", username]
    send(msg_a_envoyer, connexion_avec_serveur)
    data = recv(connexion_avec_serveur)
    disconnect(connexion_avec_serveur)
    return data


def get_msg(id):
    connexion_avec_serveur = connect(readcfg(['SOCKET', 'host']), readcfg(['SOCKET', 'port']))
    msg_a_envoyer = ["get_msg", id]
    send(msg_a_envoyer, connexion_avec_serveur)
    data = recv(connexion_avec_serveur)
    disconnect(connexion_avec_serveur)
    return data

def register(username, password, first_name, last_name, email):
    connexion_avec_serveur = connect(readcfg(['SOCKET','host']), readcfg(['SOCKET','port']))
    if connexion_avec_serveur == "err1":
        return "err1"
    else:
        msg_a_envoyer = ["register", username, password, first_name, last_name, email]
        send(msg_a_envoyer,connexion_avec_serveur)
        stringdata = recv(connexion_avec_serveur)
        disconnect(connexion_avec_serveur)
        if stringdata == "reg ok":
            return True
        else:
            return stringdata


def check_cfg():
    if os.path.exists("client_config.ini") == False:
        config = configparser.ConfigParser()
        config.read('client_config.ini')
        config['SOCKET'] = {'host': 'localhost',
                            'port': '1111'}
        with open('client_config.ini', 'w') as configfile:
            config.write(configfile)
        config['HTTP'] = {'host': 'localhost',
                          'port': '8000'}
        with open('client_config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        config = configparser.ConfigParser()
        config.read('client_config.ini')
        if ('SOCKET' in config) == False:
            os.remove("client_config.ini")
            config['SOCKET'] = {'host': 'localhost',
                                'port': '1111'}
            with open('client_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('host' in config['SOCKET']) == False:
            config['SOCKET']['host'] = 'localhost'
            with open('client_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('port' in config['SOCKET']) == False:
            config['SOCKET']['port'] = '1111'
            with open('client_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('HTTP' in config) is False:
            config['HTTP'] = {'host': 'localhost',
                              'port': '8000'}
            with open('client_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('host' in config['HTTP']) is False:
            config['SOCKET']['host'] = 'localhost'
            with open('client_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('port' in config['HTTP']) is False:
            config['SOCKET']['port'] = '8000'
            with open('client_config.ini', 'w') as configfile:
                config.write(configfile)
