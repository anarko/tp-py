import sqlite

class Crud:
    db = None

    def __init__( self ):
        self.db = sqlite.SlqliteConn()
        return None
    
    def guarda_registro( self, registro ):
        if  ( not isinstance(registro,dict) ):
            raise TypeError('TipoRegistroError')
        
        self.db.guarda_datos(registro)
        return None
    
    def busca_registro(self,registro ):
        if  ( not isinstance(registro,dict) ):
            raise TypeError('TipoRegistroError')

        r = self.db.busca_datos(registro)
        print(r)
        

    def elimina_registro(self,registro):
        if  ( not isinstance(registro,dict) ):
            raise TypeError('TipoRegistroError')

        self.db.elimina_datos(registro)
        return None

a = Crud()
#a.guarda_registro({'titulo':'titulo 3','descripcion':'desc rip1',})
a.busca_registro({'titulo':"%"})
a.elimina_registro({'titul3o':"titulo2"})
a.busca_registro({'id':"%"})