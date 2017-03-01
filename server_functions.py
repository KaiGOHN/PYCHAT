import configparser
import os.path

def login(userinput, self):
    login = str(userinput[1])
    password = (str(userinput[2]))[:-1]
    is_login_valid = check_login(login)
    if is_login_valid == True:
        is_password_valid = check_password(login, password)
        if is_password_valid == True:
            try :
                import mysql.connector
                cnx = mysql.connector.connect(host=readcfg(['DATABASE','host']),
                                              port=int(readcfg(['DATABASE','port'])),
                                              user=readcfg(['DATABASE','user']),
                                              password=readcfg(['DATABASE','password']),
                                              database=readcfg(['DATABASE','database']))
                cursor = cnx.cursor()
                log_user = ("UPDATE users "
                            "SET status = '1'"
                            "WHERE username = '" + login + "'")
                cursor.execute(log_user)
                cnx.commit()
                cursor.close()
                cnx.close()
                msg = "logs ok"
                self.clientsocket.send(msg.encode('utf-8'))
            except:
                msg = "err3"
                self.clientsocket.send(msg.encode('utf-8'))
        else:
            self.clientsocket.send(b"invalid username or password")
    else:
        self.clientsocket.send(b"invalid username or password")

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
            self.clientsocket.send(msg.encode('utf-8'))
        except:
            msg = "err3"
            self.clientsocket.send(msg.encode('utf-8'))
    else:
        msg = "err4"
        self.clientsocket.send(msg.encode('utf-8'))

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
    data = str(data)
    data = data[14:-5]
    if data != "":
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
    data = str(data)
    data = data[14:-5]
    if data != "":
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
    data = data[14:-5]
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
    if os.path.exists("server_config.ini") == False:
        config = configparser.ConfigParser()
        config.read('server_config.ini')
        config['SOCKET'] = {'host': 'localhost',
                            'port': '1111'}
        config['DATABASE'] = {'host': '',
                              'port': '',
                              'user' : '',
                              'password' : '',
                              'database': ''}
        with open('server_config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        config = configparser.ConfigParser()
        config.read('server_config.ini')
        if ('SOCKET' in config) == False:
            os.remove("server_config.ini")
            config['SOCKET'] = {'host': 'localhost',
                                'port': '1111'}
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('host' in config['SOCKET']) == False:
            config['SOCKET']['host'] = 'localhost'
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('port' in config['SOCKET']) == False:
            config['SOCKET']['port'] = '1111'
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)

        if ('host' in config['DATABASE']) == False:
            config['DATABASE']['host'] = ''
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('port' in config['DATABASE']) == False:
            config['DATABASE']['port'] = ''
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('user'in config['DATABASE']) == False:
            config['DATABASE']['user'] = ''
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('password' in config['DATABASE']) == False:
            config['DATABASE']['password'] = ''
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('database' in config['DATABASE']) == False:
            config['DATABASE']['database'] = ''
            with open('server_config.ini', 'w') as configfile:
                config.write(configfile)

