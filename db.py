import mysql.connector

class Database:
    global db
    global mycursor
    global lastGameId
    def connect_and_execute():
        
        getLastCreatedGame = 'SELECT * FROM gamecount ORDER BY ID DESC LIMIT 1'

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="1232",
            database= "tetris"
            )
        
        mycursor = db.cursor()
        mycursor.execute(getLastCreatedGame);
        myresult = (mycursor.fetchall())
        temp = myresult[0][1]
        print("connetced and temp iss ",temp)
        lastGameId= temp+1        
        sql = f"INSERT INTO gamecount(game_table) VALUES ('{lastGameId}')"
        mycursor.execute(sql)
        db.commit()
        
        sql1 = f"CREATE TABLE input_{lastGameId} (type varchar(255), tick varchar(255), move varchar(255)); "
        mycursor.execute(sql1)
        db.commit()
        
    def connect_and_save():
        print("exectuing this")
        f = open("temp.txt", "r")
        print("file opeend")
        for x in f:
            print("we in the for loop")
            temp2 = x.split(',')
            print("This is temp2" - str(temp2))
            print(temp2[0],temp2[1],temp2[3])
            sqltype = f"INSERT INTO input_{lastGameId} VALUES ('{temp2[0]},{temp2[1]},{temp2[2]}')"
            mycursor.execute(sqltype)
            db.commit()
        f.close()

