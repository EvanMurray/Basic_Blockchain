import sqlite3 as lite


class Database:
    def __init__(self):
        self.db_name = "blockchain.db"
        self.db_connection = lite.connect(self.db_name)



    def init_db(self):
        
        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Blockchain (chain TEXT, transactions TEXT)")
            cursor.close()
            
            

    def fetch_db(self):
        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM Blockchain")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            cursor.close()
