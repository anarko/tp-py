#Library import
import re
from tkinter import  StringVar

class StrVarConValidador(StringVar):
    ''' Extiende la clase StringVar de Tk para agregarle validaciones '''
    
    def validar_alfanumerico(self):
        ''' valida que el contenido de la variable se aun alfanumerico '''
        if re.fullmatch("^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$",self.get()) is None:
            return False
        return True        

    def validar_no_vacio(self):
        ''' valida que no este vacia la variable '''
        if len(self.get()) == 0:
             return False
        return True
        