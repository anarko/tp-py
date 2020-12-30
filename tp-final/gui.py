import tkinter
import crud_sqlite

''' 
    TODO : exeptions 
           form para editar/guardar
           regex para entrada de datos
'''

class CrudTk(tkinter.Frame):
    ''' Extiende la clase Framne de tk para poder manejar los contenedores y contenidos del crud '''

    def __init__(self, master):
        tkinter.Frame.__init__(self, master,height=300, width=100)
        # coneccion a la base de datos
        self.db = crud_sqlite.CrudSqlite()
        # Menu principal
        self.mainmenu = tkinter.Menu(master)
        self.mainmenu.add_command(label = "Nuevo", command= self.__frm_nuevo_registro__)  
        self.mainmenu.add_command(label = "Buscar", command= self.__frm_buscar_registro__)
        self.mainmenu.add_command(label = "Exit", command= master.destroy)
        master.config(menu = self.mainmenu)     
        self.__frm_nuevo_registro__()

    def __frm_nuevo_registro__(self):
        ''' Arma el form para cargar un nuevo registro '''
        self.__vacia_form__()
        lf = tkinter.LabelFrame(self, fg="green", font=( '', 11, 'bold'), text="Nuevo registro")       
        tkinter.Label(lf, text = "Título",width = 20).pack()
        self.titulo = tkinter.Entry(lf, width = 20)
        self.titulo.pack(padx = 5, pady = 5)   
        tkinter.Label(lf, text = "Descripcion", width = 20).pack()
        self.descripcion = tkinter.Entry(lf, width = 20)
        self.descripcion.pack(padx = 5, pady = 5)   
        tkinter.Button(lf, text = "Guardar", command=self.__guardar_registro__).pack(padx = 3, pady = 3)
        lf.pack(fill="both")

    def __frm_buscar_registro__(self):
        ''' Arma el form para buscar un nuevo '''
        self.__vacia_form__()
        lf = tkinter.LabelFrame(self, fg="green", font=( '', 11, 'bold'), text="Buscar registro")       
        tkinter.Label(lf, text = "Título",width = 20).pack()
        self.titulo = tkinter.Entry(lf, width = 20)
        self.titulo.pack(padx = 5, pady = 5)   
        tkinter.Label(lf, text = "Descripcion", width = 20).pack()
        self.descripcion = tkinter.Entry(lf, width = 20)
        self.descripcion.pack(padx = 5, pady = 5)   
        tkinter.Button(lf, text = "Buscar", command=self.__buscar_registro__).pack(padx = 3, pady = 3)
        lf.pack(fill="both")

    def __vacia_form__(self):
        ''' destruye los elementos del form '''        
        for cosa in self.winfo_children():
            cosa.destroy()
        

    def __guardar_registro__(self):
        ''' Guarda los datos integresados en la base de datos, si existen los reemplaza '''
        print(self.titulo.get())

    def __buscar_registro__(self):
        ''' Busca uno o mas registros en la base de datos '''
        pass



if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Crud y ques")
    CrudTk(root).pack(fill="both")
    root.mainloop()

