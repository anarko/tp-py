import sqlite

class crud:
    db = None

    def __init__( self ):
        self.db = sqlite.slqliteConn()
        return None
    
    def guarda_registro( self, registro ):
        if  ( not isinstance(registro,dict) ):
            raise NameError('tipo_erroneo')
        
        self.db.guarda_datos(registro)
        return None
    
    def busca_registro(self,registro ):
        if  ( not isinstance(registro,dict) ):
            raise NameError('tipo_erroneo')

        r = self.db.busca_datos(registro)
        print(r)
        

    def elimina_registro(self,registro):
        if  ( not isinstance(registro,dict) ):
            raise NameError('tipo_erroneo')

        self.db.elimina_datos(registro)
        return None

a = crud()
#a.guarda_registro({'titulo':'titulo 3','descripcion':'desc rip1',})
a.busca_registro({'titulo':"%"})
a.elimina_registro({'titul3o':"titulo2"})
a.busca_registro({'id':"%"})