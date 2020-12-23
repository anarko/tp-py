import sqlite3


class slqliteConn:
    rec = None

    def __init__(self, fileName="default.db"):
        try:
            self.rec = sqlite3.connect(fileName)
        except:
            print("Error accediendo/creando la base de datos")
        
        return None