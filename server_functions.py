import configparser
import os.path
import pickle

def login(userinput, self):
    login = str(userinput[1])
    password = str(userinput[2])
    is_login_valid = check_login(login)
    if is_login_valid == True:
        is_password_valid = check_password(login, password)
        if is_password_valid == True:
            try :
                import mysql.connector
                cnx = mysql.connector.connect(host=readcfg(['DATABASE', 'host']),
                                              port=int(readcfg(['DATABASE', 'port'])),
                                              user=readcfg(['DATABASE', 'user']),
                                              password=readcfg(['DATABASE', 'password']),
                                              database=readcfg(['DATABASE', 'database']))
                cursor = cnx.cursor()
                log_user = ("UPDATE users "
                            "SET status = '1'"
                            "WHERE username = '" + login + "'")
                cursor.execute(log_user)
                cnx.commit()
                cursor.close()
                cnx.close()
                msg = "logs ok"
                self.clientsocket.send(pickle.dumps(msg))
            except:
                msg = "err3"
                self.clientsocket.send(pickle.dumps(msg))
        else:
            self.clientsocket.send(pickle.dumps("invalid username or password"))
    else:
        self.clientsocket.send(pickle.dumps("invalid username or password"))


def sendmsg(userinput, self):
    import time
    username = str(userinput[1])
    msg = str(userinput[2])
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        import mysql.connector
        cnx = mysql.connector.connect(host=readcfg(['DATABASE', 'host']),
                                      port=int(readcfg(['DATABASE', 'port'])),
                                      user=readcfg(['DATABASE', 'user']),
                                      password=readcfg(['DATABASE', 'password']),
                                      database=readcfg(['DATABASE', 'database']))
        cursor = cnx.cursor()
        query = "INSERT INTO chat (username, msg, time) VALUES(" + "'" + username + "'" + ", " + "'" + msg + "'" + ", " + "'" + time + "'" + ")"
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()



    except:
        msg = "err3"
        self.clientsocket.send(pickle.dumps(msg))


def loadidslist(username, self):
    try:
        import mysql.connector
        import time
        cnx = mysql.connector.connect(host=readcfg(['DATABASE', 'host']),
                                      port=int(readcfg(['DATABASE', 'port'])),
                                      user=readcfg(['DATABASE', 'user']),
                                      password=readcfg(['DATABASE', 'password']),
                                      database=readcfg(['DATABASE', 'database']))
        cursor = cnx.cursor()
        query = "SELECT id FROM chat ORDER BY id ASC"
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.commit()
        cursor.close()
        if data != "":
            self.clientsocket.send(pickle.dumps(data))
        else:
            self.clientsocket.send(pickle.dumps("nomessages"))
    except:
        self.clientsocket.send(pickle.dumps("err3"))

def get_msg(userinput, self):
    id = str(userinput[1])
    try:
        import mysql.connector
        cnx = mysql.connector.connect(host=readcfg(['DATABASE', 'host']),
                                      port=int(readcfg(['DATABASE', 'port'])),
                                      user=readcfg(['DATABASE', 'user']),
                                      password=readcfg(['DATABASE', 'password']),
                                      database=readcfg(['DATABASE', 'database']))
        cursor = cnx.cursor()
        query = "SELECT username FROM chat WHERE id ='" + id + "'"
        cursor.execute(query)
        username = cursor.fetchall()
        username = str(username[0])
        username = username[2:-3]
        query = "SELECT msg FROM chat WHERE id ='" + id + "'"
        cursor.execute(query)
        msg = cursor.fetchall()
        msg = str(msg[0])
        msg = msg[2:-3]
        query = "SELECT time FROM chat WHERE id ='" + id + "'"
        cursor.execute(query)
        time = cursor.fetchall()
        time = str(time[0])
        time = time[19:-3]
        time = time.split(", ")
        time = str(time[3] + ":" + time[4] + ":" + time[5])
        returnlist = [id, username, msg, time]

        self.clientsocket.send(pickle.dumps(returnlist))
    except:
        self.clientsocket.send(pickle.dumps("err3"))

def register(userinput, self):
    username = str(userinput[1])
    password = str(userinput[2])
    first_name = str(userinput[3])
    last_name = str(userinput[4])
    email = (str(userinput[5]))[:-1]
    is_login_used = check_login(username)
    is_email_used = check_email(email)
    if is_email_used == False and is_login_used == False:
        try:
            import mysql.connector
            cnx = mysql.connector.connect(host=readcfg(['DATABASE', 'host']),
                                          port=int(readcfg(['DATABASE', 'port'])),
                                          user=readcfg(['DATABASE', 'user']),
                                          password=readcfg(['DATABASE', 'password']),
                                          database=readcfg(['DATABASE', 'database']))
            cursor = cnx.cursor()
            query = "INSERT INTO users (password, username, first_name, last_name, email) VALUES(" + "'" + password + "'" + ", " + "'" + username + "'" + ", " + "'" + first_name + "'" + ", " + "'" + last_name + "'" + ", " + "'" + email + "'" +")"
            cursor.execute(query)
            cnx.commit()
            cursor.close()
            cnx.close()
            msg = "reg ok"
            self.clientsocket.send(pickle.dumps(msg))
        except:
            msg = "err3"
            self.clientsocket.send(pickle.dumps(msg))
    else:
        msg = "err4"
        self.clientsocket.send(pickle.dumps(msg))

def check_login(login):
    import mysql.connector
    cnx = mysql.connector.connect(host=readcfg(['DATABASE', 'host']),
                                  port=int(readcfg(['DATABASE', 'port'])),
                                  user=readcfg(['DATABASE', 'user']),
                                  password=readcfg(['DATABASE', 'password']),
                                  database=readcfg(['DATABASE', 'database']))
    cursor = cnx.cursor()
    query = "SELECT username FROM users WHERE username ='" + login + "'"
    cursor.execute(query)
    data = cursor.fetchall()
    if data != []:
        cursor.close()
        cnx.close()
        return True
    else:
        return False

def check_email(email):
    import mysql.connector
    cnx = mysql.connector.connect(host=readcfg(['DATABASE', 'host']),
                                  port=int(readcfg(['DATABASE', 'port'])),
                                  user=readcfg(['DATABASE', 'user']),
                                  password=readcfg(['DATABASE', 'password']),
                                  database=readcfg(['DATABASE', 'database']))
    cursor = cnx.cursor()
    query = "SELECT username FROM users WHERE email ='" + email + "'"
    cursor.execute(query)
    data = cursor.fetchall()
    if data != []:
        cursor.close()
        cnx.close()
        return True
    else:
        return False


def check_password(login,password):
    import mysql.connector
    cnx = mysql.connector.connect(host=readcfg(['DATABASE', 'host']),
                                  port=int(readcfg(['DATABASE', 'port'])),
                                  user=readcfg(['DATABASE', 'user']),
                                  password=readcfg(['DATABASE', 'password']),
                                  database=readcfg(['DATABASE', 'database']))
    cursor = cnx.cursor()
    query = "SELECT password FROM users WHERE username ='" + login + "'"
    cursor.execute(query)
    data = cursor.fetchall()
    data = str(data)
    data = data[3:-4]
    if data == password:
        cursor.close()
        cnx.close()
        return True
    else:
        return False


def readcfg(list):
    config = configparser.ConfigParser()
    config.read('server_config.ini')
    for item in list:
        config = config[item]
    return str(config)

def check_cfg():
    if os.path.exists("server_config.ini") is False:
        config = configparser.ConfigParser()
        config.read('server_config.ini')
        config['SOCKET'] = {'host': 'localhost',
                            'port': '1111'}
        config['DATABASE'] = {'host': '',
                              'port': '',
                              'user' : '',
                              'password' : '',
                              'database': ''}
    else:
        config = configparser.ConfigParser()
        config.read('server_config.ini')
        if ('SOCKET' in config) is False:
            config['SOCKET'] = {'host': 'localhost',
                                'port': '1111'}
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('host' in config['SOCKET']) is False:
            config['SOCKET']['host'] = 'localhost'
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('port' in config['SOCKET']) is False:
            config['SOCKET']['port'] = '1111'
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('host' in config['DATABASE']) is False:
            config['DATABASE']['host'] = ''
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('port' in config['DATABASE']) is False:
            config['DATABASE']['port'] = ''
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('user' in config['DATABASE']) is False:
            config['DATABASE']['user'] = ''
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('password' in config['DATABASE']) is False:
            config['DATABASE']['password'] = ''
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('database' in config['DATABASE']) is False:
            config['DATABASE']['database'] = ''
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)

