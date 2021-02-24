#Library import
import sqlite3
import datetime

class CrudSqlite:
    """ Clase para conexion y manejo de la base de datos sqlite3 """
    rec = None

    def __init__(self, fileName="default.db"):
        try:
            self.rec = sqlite3.connect(fileName)
        except:            
            self.rec = None #limpio la coneccion por las dudas
            raise RuntimeError("Error accediendo/creando la base de datos")            
        self.crear_tabla(drop=False)
        return None

    def crear_tabla(self,drop=False):
        """ Crea la tabla si no existe, si se pasa el parametro drop=true la borra y crea de nuevo """
        
        self.cur = self.rec.cursor()
        if drop: 
            self.cur.execute('DROP TABLE IF EXISTS mascotas')        
            self.rec.commit()
        self.cur.execute('CREATE TABLE IF NOT EXISTS mascotas ( id INTEGER PRIMARY KEY AUTOINCREMENT, nombre VARCHAR(128)  NOT NULL, raza varchar(128) NOT NULL, vacunas varchar (128)NOT NULL, tipo varchar (128), fecha datetime )')
        self.rec.commit()

    def nueva_tabla(self):
        """ Alias de crear_tabla """

        self.crear_tabla(True)

    def guarda_datos(self, registro):
        """ Recibe un dict como registro de datos e intenta guardarlo como nuevo, si existe actualiza el registro"""

        if ( not self.rec ):
            raise RuntimeError("Base de datos no prensete")
        if ( not isinstance(registro,dict) ):
            raise TypeError('TipoRegistroError')
        
        registro['fecha'] = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        if "id" in registro:
            query = "UPDATE mascotas SET nombre = :nombre,  raza = :raza, vacunas = :vacunas, tipo = :tipo, fecha = :fecha WHERE id = :id"
        else:
            query = "INSERT INTO mascotas (nombre, raza, vacunas, tipo, fecha) VALUES (:nombre, :raza, :vacunas, :tipo, :fecha)"
        
        self.cur.execute(query,registro)
        self.rec.commit()
        return None
    
    def busca_datos(self,registro):
        """ 
            Recibe un dict como registro de datos y busca en base a los datos del registro. 
            Devuelve una lista de diccionarios con los registros encontrados
        """

        if ( not self.rec ):
            raise RuntimeError("Base de datos no prensete")
        if ( not isinstance(registro,dict) ):
               raise TypeError('TipoRegistroError')
        campos,valores,resultset = "",[],[]
        for cosa in registro:
            if str(registro.get(cosa)) != "":
                campos += cosa +" like :"+cosa+" AND "
                valores.append("%"+str(registro.get(cosa))+"%")
        query = "SELECT * FROM mascotas WHERE "+campos[:-4]+" ORDER By fecha"

        self.cur.execute(query,valores)
        for x in self.cur.fetchall():
            resultset.append(x)
        return resultset
    
    def elimina_datos(self,registro):
        """ Recibe un dict como registro de datos y elimina de la base de datos en base al registro """

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
