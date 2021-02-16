import sqlite3
import datetime

class CrudSqlite:
    ''' Clase para conexion y manejo de la base de datos sqlite3 '''
    rec = None

    def __init__(self, fileName="default.db"):
        try:
            self.rec = sqlite3.connect(fileName)
           
        except:            
            self.rec = None #limpio la coneccion por las dudas
            raise RuntimeError("Error accediendo/creando la base de datos")            
        self.crear_tabla(drop=False)
        return None
    
    def vacia_base_datos(self):
        """ Reinicia la base de datos """
        valor = messagebox.askquestion(
            "Restarurar", "Esta seguro de que desea borrar todos los datos?"
        )
        if valor == "yes":
            self.nueva_tabla()

    def crear_tabla(self,drop=False):
        ''' Crea la tabla si no existe, si se pasa el parametro drop=true la borra y crea de nuevo '''
        self.cur = self.rec.cursor()
        if drop: 
            self.cur.execute('DROP TABLE IF EXISTS mascotas')        
            self.rec.commit()
        self.cur.execute('CREATE TABLE IF NOT EXISTS mascotas ( id INTEGER PRIMARY KEY AUTOINCREMENT, nombre VARCHAR(128)  NOT NULL, raza varchar(128) NOT NULL, vacunas varchar (128)NOT NULL, tipo varchar (128), fecha datetime )')
        self.rec.commit()

    def nueva_tabla(self):
        ''' Alias de crear_tabla '''
        self.crear_tabla(True)

    def guarda_datos(self, registro):
        ''' Recibe un dict como registro de datos e intenta guardarlo como nuevo '''

        if ( not self.rec ):
            raise RuntimeError("Base de datos no prensete")
        if ( not isinstance(registro,dict) ):
            raise TypeError('TipoRegistroError')
        
        registro['fecha'] = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        query = "INSERT INTO mascotas (nombre, raza, vacunas, tipo, fecha) VALUES (:nombre, :raza, :vacunas, :tipo, :fecha)"
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
            if str(registro.get(cosa)) != "":
                campos += cosa +" like :"+cosa+" OR "
                valores.append("%"+str(registro.get(cosa))+"%")
        query = "SELECT * FROM mascotas WHERE "+campos[:-4]
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
        query = "DELETE FROM mascotas WHERE "+campos[:-5]
        self.cur.execute(query,valores)
        self.rec.commit()
        return None 
    
    def nuevo_Registro(self, registro):
        ''' Recibe un dict como registro de datos e intenta guardarlo como nuevo, si existe actualiza título y descripción '''

        if ( not self.rec ):
            raise RuntimeError("Base de datos no prensete")
        if ( not isinstance(registro,dict) ):
            raise TypeError('TipoRegistroError')
        
        registro['fecha'] = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")

        query = """INSERT INTO mascotas (nombre, raza, vacunas, tipo, fecha) 
        VALUES (:nombre, :raza, :vacunas, :tipo, :fecha)"""

        self.cur.execute(query,registro)
        self.rec.commit()
        return True

    def edita_datos(self, registro):
        ''' Recibe un dict como registro de datos y hace update en la base de datos '''

        if ( not self.rec ):
            raise RuntimeError("Base de datos no prensete")
        if ( not isinstance(registro,dict) ):
               raise TypeError('TipoRegistroError')           
        
        query = "UPDATE mascotas SET nombre = ?, raza = ?, vacunas = ? , tipo = ? WHERE id = " + str(registro['id'])
        valores = (str(registro['nombre']), str(registro['raza']), str(registro['vacunas']), str(registro['tipo']))
        self.cur.execute(query, valores)
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