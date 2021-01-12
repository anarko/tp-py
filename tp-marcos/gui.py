import re
import tkinter
import crud_sqlite

''' 
    TODO : exeptions 
           form para editar/guardar
'''

class CrudTk(tkinter.Frame):
    ''' Extiende la clase Frame de tk para poder manejar los contenedores y contenidos del crud '''

    def __init__(self, master):
        tkinter.Frame.__init__(self, master,height=300, width=100)
        # coneccion a la base de datos
        self.db = crud_sqlite.CrudSqlite()
        # Menu principal
        self.mainmenu = tkinter.Menu(master)
        self.mainmenu.add_command(label = "Nuevo", command= self._frm_nuevo_registro)  
        self.mainmenu.add_command(label = "Buscar", command= self._frm_buscar_registro)
        self.mainmenu.add_command(label = "Exit", command= master.destroy)
        master.config(menu = self.mainmenu)     
        self._frm_nuevo_registro()

    def _frm_blanco(self):
        ''' Arma el form para cargar un nuevo registro '''
        self._vacia_form()
        self.lf = tkinter.LabelFrame(self, fg="green", font=( '', 11, 'bold'), text="Nuevo registro")       
        tkinter.Label(self.lf, text = "Título",width = 20).pack()
        self.titulo = tkinter.Entry(self.lf, width = 20)
        self.titulo.pack(padx = 5, pady = 5)   
        tkinter.Label(self.lf, text = "Descripcion", width = 20).pack()
        self.descripcion = tkinter.Entry(self.lf, width = 20)
        self.descripcion.pack(padx = 5, pady = 5)   
        
        self.lf.pack(fill="both")
    
    def _frm_nuevo_registro(self):        
        self._frm_blanco()
        tkinter.Button(self.lf, text = "Guardar", command=self._guardar_registro).pack(padx = 3, pady = 3)

    def _frm_buscar_registro(self):
        ''' Arma el form para buscar un nuevo '''
        self._vacia_form()
        lf = tkinter.LabelFrame(self, fg="green", font=( '', 11, 'bold'), text="Buscar registro")       
        tkinter.Label(lf, text = "Título",width = 20).pack()
        self.titulo = tkinter.Entry(lf, width = 20)
        self.titulo.pack(padx = 5, pady = 5)   
        tkinter.Label(lf, text = "Descripcion", width = 20).pack()
        self.descripcion = tkinter.Entry(lf, width = 20)
        self.descripcion.pack(padx = 5, pady = 5)   
        tkinter.Button(lf, text = "Buscar", command=self._buscar_registro).pack(padx = 3, pady = 3)
        lf.pack(fill="both")

    def _vacia_form(self):
        ''' destruye los elementos del form '''        
        for cosa in self.winfo_children():
            cosa.destroy()
        
    def _guardar_registro(self):
        ''' Guarda los datos integresados en la base de datos, si existen los reemplaza '''
        
        # Busca que el titulo sea solo alfanumerico        
        if re.fullmatch("^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$",self.titulo.get()) is None:
            print("Error solo letras y nros : ",self.titulo.get())            
            return        

    def _buscar_registro(self):
        ''' Busca uno o mas registros en la base de datos '''
        r = {'titulo':self.titulo.get(),'descripcion':self.descripcion.get()}
        resp = self.db.busca_datos(r)
        if len(resp)  == 1:
            self._frm_nuevo_registro()
            self.titulo.delete(0,tkinter.END)
            self.titulo.insert(0,resp[0].get('titulo'))
            self.descripcion.insert(0,resp[0].get('descripcion'))
        

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Crud y ques")
    CrudTk(root).pack(fill="both")
    root.mainloop()

