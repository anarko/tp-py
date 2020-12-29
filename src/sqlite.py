import sqlite3


class SlqliteConn:
    rec = None

    def __init__(self, fileName="default.db"):
        try:
            self.rec = sqlite3.connect(fileName)
            self.rec.row_factory = dict_factory
            self.cur = self.rec.cursor()
            self.cur.execute('CREATE TABLE IF NOT EXISTS datos(id integer, titulo text, descripcion text, PRIMARY KEY("id" AUTOINCREMENT))')
            self.cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_titulo ON datos (titulo)')
        except:
            print("Error accediendo/creando la base de datos")
        return None
    
    def guarda_datos(self, d):
        campos,valores = "",""
        for cosa in d:
            campos += cosa +','
            valores += ":"+cosa+"," 
        query = "INSERT INTO datos ("+campos[:-1]+") VALUES ("+valores[:-1]+")"        
        self.cur.execute(query,d)
        self.rec.commit()
        return None
    
    def busca_datos(self,d):
        campos,valores,resultset = "",[],[]
        for cosa in d:
            campos += cosa +" like :"+cosa+" OR "
            valores.append("%"+str(d.get(cosa))+"%")
        query = "SELECT * FROM datos WHERE "+campos[:-4]
        self.cur.execute(query,valores)
        for x in self.cur.fetchall():
            resultset.append(x)
        return resultset
    
    def elimina_datos(self,d):
        campos,valores = "",[]
        for cosa in d:
            campos += cosa +"=:"+cosa+" AND "
            valores.append(str(d.get(cosa)))       
        query = "DELETE FROM datos WHERE "+campos[:-5]
        self.cur.execute(query,valores)
        self.rec.commit()
        return None


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
            
        