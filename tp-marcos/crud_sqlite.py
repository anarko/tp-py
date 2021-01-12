import sqlite3

class CrudSqlite:
    ''' Clase para conexion y manejo de la base de datos sqlite3 '''
    rec = None

    def __init__(self, fileName="default.db"):
        try:
            self.rec = sqlite3.connect(fileName)
            self.rec.row_factory = _dict_factory
            self.cur = self.rec.cursor()
            self.cur.execute('CREATE TABLE IF NOT EXISTS datos(id integer, titulo text, descripcion text, PRIMARY KEY("id" AUTOINCREMENT))')
            self.cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_titulo ON datos (titulo)')
        except:            
            self.rec = None #limpio la coneccion por las dudas
            print("Error accediendo/creando la base de datos")
        return None
    
    def guarda_datos(self, registro):
        ''' Recibe un dict como registro de datos e intenta guardarlo como nuevo, si existe actualiza título y descripción '''

        if ( not self.rec ):
            raise RuntimeError("Base de datos no prensete")
        if ( not isinstance(registro,dict) ):
            raise TypeError('TipoRegistroError')
        
        query = "INSERT INTO datos (titulo,descripcion) VALUES (:titulo,:descripcion) \
                 ON CONFLICT(titulo) DO UPDATE SET titulo=:titulo, descripcion=:descripcion"
        self.cur.execute(query,registro)
        self.rec.commit()
        return None
    
    def busca_datos(self,registro):
        ''' 
            Recibe un dict como registro de datos y busca en base a los datos del registro. 
            Devuelve una lista de diccionarios con los registros encontrados
        '''

        if ( not self.rec ):
            raise RuntimeError("Base de datos no prensete")
        if ( not isinstance(registro,dict) ):
               raise TypeError('TipoRegistroError')
        campos,valores,resultset = "",[],[]
        for cosa in registro:
            print(cosa)
            if str(registro.get(cosa)) != "":
                campos += cosa +" like :"+cosa+" OR "
                valores.append("%"+str(registro.get(cosa))+"%")
        query = "SELECT * FROM datos WHERE "+campos[:-4]
        print(query,valores)
        self.cur.execute(query,valores)
        for x in self.cur.fetchall():
            resultset.append(x)
        return resultset
    
    def elimina_datos(self,registro):
        ''' Recibe un dict como registro de datos y elimina de la base de datos en base al registro '''

        if ( not self.rec ):
            raise RuntimeError("Base de datos no prensete")
        if ( not isinstance(registro,dict) ):
               raise TypeError('TipoRegistroError')           
        campos,valores = "",[]
        for cosa in registro:
            if str(registro.get(cosa)) != "":
                campos += cosa +"=:"+cosa+" AND "
                valores.append(str(registro.get(cosa)))
        query = "DELETE FROM datos WHERE "+campos[:-5]
        self.cur.execute(query,valores)
        self.rec.commit()
        return None 
    

def _dict_factory(cursor, row):
    ''' Reemplaza el generador originael de SQLite3 por uno que devuelve un dict '''
      
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    

if __name__ == "__main__":
    ''' test module functions '''

    a = CrudSqlite()
    a.guarda_datos({'titulo':'titulo 2','descripcion':'descrip2'})
    print(a.busca_datos({'titulo':"%"}))
