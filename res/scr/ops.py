from mariadb import *
from json import load
import mariadb

def read_json(filepath:str):
    """
    Reads json loacated in filepath
    """
    with open(mode="r", file=filepath, encoding="utf-8") as conf:
        return load(conf)


class NoMariaArgs(Exception):
    def __init__(self):
        return "MariaConnection object has no args while creating"


class MariaConnection:
    def __init__(self, args:dict):
        """
        Creates mariadb connection
        :param args: should be host, port, user, password, db
        """
        if args != {}:
            self.mariaconnection = mariadb.connect(**args)
            self.cursor = Cursor(self.mariaconnection)
            self.mariaconnection.autocommit = True
        else:
            raise NoMariaArgs
        
    def get_conn(self):
        return self.mariaconnection
    
    def get_curr(self):
        return self.cursor
    

class Users:
    def __init__(self, mariaconnection: MariaConnection):
        """
        Table users ops here
        :param mariaconnection: MariaConnection object
        """
        self.mariaconnection = mariaconnection
        self.queries = {
            "get_by_username": "SELECT * FROM users WHERE username = ?;",
            "get_by_email": "SELECT * FROM users WHERE email = ?;",
            "insert_with_username": "INSERT INTO users (username, id, email) VALUES (?, ?, ?);",
            "get_all_ids": "SELECT DISTINCT id FROM users;",
            "change_email": "UPDATE users SET email = ? WHERE username = ?;"
        }

    def get_by_username(self, username:str):
        self.mariaconnection.cursor.execute(self.queries["get_by_username"], [username])
        return self.mariaconnection.cursor.fetchone()

    def get_by_email(self, email:str):
        self.mariaconnection.cursor.execute(self.queries["get_by_email"], [email])
        return self.mariaconnection.cursor.fetchone()

    def change_email(self, username, new_email):
        self.mariaconnection.cursor.execute(self.queries["change_email"], [new_email, username])
        
    
    def insert_with_username(self, username:str, id:str, email:str):
        self.mariaconnection.cursor.execute(self.queries["insert_with_username"], [username, id, email])

    def get_all_telegramms(self):
        self.mariaconnection.cursor.execute(self.queries["get_all_ids"])
        return self.mariaconnection.cursor.fetchall()
