import mysql.connector

class Database:
    global db
    global mycursor
    global lastGameId
    
    def connect_and_execute():
        getLastCreatedGame = 'SELECT * FROM gamecount ORDER BY ID DESC LIMIT 1'
        db = mysql.connector.connect(
            host="sql11.freemysqlhosting.net",
            user="sql11498615", 
            passwd="Zc15ynVuIw",
            database= "sql11498615"
            )
        mycursor = db.cursor()
        mycursor.execute(getLastCreatedGame);
        myresult = (mycursor.fetchall())
        temp = myresult[0][1]
        print("connetced and temp iss ",temp)
        global lastGameId
        lastGameId= temp+1        
        sql = f"INSERT INTO gamecount(game_table) VALUES ('{lastGameId}')"
        mycursor.execute(sql)
        db.commit()
        
            
        sql1 = f"CREATE TABLE input_{lastGameId} (type varchar(255), tick varchar(255), move varchar(255)); "
        mycursor.execute(sql1)
        db.commit()
        
    def connect_and_save():        
        db = mysql.connector.connect(
            host="sql11.freemysqlhosting.net",
            user="sql11498615", 
            passwd="Zc15ynVuIw",
            database= "sql11498615"
            )
        
        mycursor = db.cursor()
        print("exectuing this")
        f = open("temp.txt", "r")
        print("file opeend")
        for x in f:
            temp2 = x.split(',')
            sqltype = f"INSERT INTO input_{lastGameId} VALUES ('{temp2[0]}','{temp2[1]}','{temp2[2]}')"
            mycursor.execute(sqltype)
            db.commit()
        f.close()
        

