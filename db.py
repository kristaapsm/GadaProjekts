import mysql.connector

class Database:
    def connect():
        db = mysql.connector.connect(
            host = "localhost",
            user="root",
            passwd="1232",
            database= "tetris"
        )
        print(db) 