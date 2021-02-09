""" INCLUIMOS LO REFERENTE A LA REPRESENTACION VISUAL DE LA APP"""

# IMPORTACIONES SEGUN PEP8

from tkinter import Tk
from tkinter import Menu
from tkinter import ttk
from tkinter import mainloop
from tkinter import Frame
from tkinter import Button
from tkinter import PhotoImage
from tkinter import Scrollbar
from tkinter import LabelFrame
from tkinter import Label
from tkinter import Canvas
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import StringVar 
from tkinter import Entry
from tkinter.constants import BOTTOM
from tkinter.constants import HORIZONTAL
from tkinter.constants import VERTICAL
from tkinter.constants import N
from tkinter.constants import S, W, E
from PIL import Image
from PIL import ImageTk
from datetime import datetime
from tkinter.colorchooser import askcolor
from modelo import CrudSqlite
from logica import logica_App

class gui:
    # CONSTRUCTOR DE LA CLASE --METODO QUE SE LEE AL INSTANCIARLA--
    def __init__(self, root, x=0.01, y=0.01, h=0.17, w=0.98):
        self.root = root
        self.master = Frame(root, bg="papaya whip")
        self.master.place(relx=x, rely=y, relheight=h, relwidth=w)
        # CREACION DE LOS WIDGETS
        self.recursos()  
        self.crear_Botones()  
        self.crear_Treeview() 
        self.status_Bar()
        self.crear_Menu()
        self.tema(kwargs='inicio')

    def recursos(self):

        self.tipo_animal = ["FELINO", "CANINO", "REPTIL", "AVE", "INSECTO", "PEZ"]

        self.img_Nuevo = Image.open("src/019-add.png")
        self.img_Nuevo = ImageTk.PhotoImage(self.img_Nuevo)

        self.img_Edit = Image.open("src/018-edit.png")
        self.img_Edit = ImageTk.PhotoImage(self.img_Edit)

        self.img_Eliminar = Image.open("src/015-remove.png")
        self.img_Eliminar = ImageTk.PhotoImage(self.img_Eliminar)

        self.img_Buscar = Image.open("src/027-search.png")
        self.img_Buscar = ImageTk.PhotoImage(self.img_Buscar)

        self.img_VerTodo = Image.open("src/005-infographic.png")
        self.img_VerTodo = ImageTk.PhotoImage(self.img_VerTodo)

        self.img_Limpiar = Image.open("src/023-remove.png")
        self.img_Limpiar = ImageTk.PhotoImage(self.img_Limpiar)

        self.img_Restaurar = Image.open("src/024-reload.png")
        self.img_Restaurar = ImageTk.PhotoImage(self.img_Restaurar)

        self.img_Tema = Image.open("src/028-setting.png")
        self.img_Tema = ImageTk.PhotoImage(self.img_Tema)

        self.img_Salir = Image.open("src/icon_cancelar.png")
        self.img_Salir = ImageTk.PhotoImage(self.img_Salir)

        # CREAMOS UN FRAME INFERIOR PARA EL INFO

    def status_Bar(self):
            
        self.infoFrame = LabelFrame(self.root, bg="black", bd=1, height=100)
        self.infoFrame.place(relx=0, rely=0.96, relheight=0.04, relwidth=1)
        self.infoLbl = Label(
            self.infoFrame, text="", font=("", 11, "bold"), fg="white", bg="black"
        )
        self.infoLbl.grid(column=0, row=0, padx=4, pady=4, sticky="W")

    def crear_Botones(self):

        self.btn_Nuevo = Button(
            self.master,
            text="NUEVO",
            bg="gray90",
            fg='black',
            font=("Arial bold", 10),
            image=self.img_Nuevo,
            compound="top",
            command=lambda: self.nuevo(),
        )
        self.btn_Nuevo.place(relx=0, rely=0, relheight=1, relwidth=0.105)

        self.btn_Editar = Button(
            self.master,
            text="EDITAR",
            bg="gray90",
            fg='black',
            font=("Arial bold", 10),
            image=self.img_Edit,
            compound="top",
            command=lambda: self.editar(),
        )
        self.btn_Editar.place(relx=0.11, rely=0, relheight=1, relwidth=0.105)

        self.btn_Eliminar = Button(
            self.master,
            text="ELIMINAR",
            bg="gray90",
            fg='black',
            font=("Arial bold", 10),
            image=self.img_Eliminar,
            compound="top",
            command=lambda: self.eliminar(),
        )
        self.btn_Eliminar.place(relx=0.22, rely=0, relheight=1, relwidth=0.105)

        self.btn_Buscar = Button(
            self.master,
            text="BUSCAR",
            bg="gray90",
            fg='black',
            font=("Arial bold", 10),
            image=self.img_Buscar,
            compound="top",
            command=lambda: self.buscar(),
        )
        self.btn_Buscar.place(relx=0.33, rely=0, relheight=1, relwidth=0.105)

        self.btn_VerTodo = Button(
            self.master,
            text="VER TODO",
            bg="gray90",
            fg='black',
            font=("Arial bold", 10),
            image=self.img_VerTodo,
            compound="top",
            command=lambda: self.ver_todos(),
        )
        self.btn_VerTodo.place(relx=0.44, rely=0, relheight=1, relwidth=0.105)

        self.btn_Limpiar = Button(
            self.master,
            text="LIMPIAR",
            bg="gray90",
            fg='black',
            font=("Arial bold", 10),
            image=self.img_Limpiar,
            compound="top",
            command=lambda: self.limpiar(),
        )
        self.btn_Limpiar.place(relx=0.55, rely=0, relheight=1, relwidth=0.105)

        self.btn_Restaurar = Button(
            self.master,
            text="RESTAURAR",
            bg="gray90",
            fg='black',
            font=("Arial bold", 10),
            image=self.img_Restaurar,
            compound="top",
            command=lambda: self.vacia_base_datos(),
        )
        self.btn_Restaurar.place(relx=0.66, rely=0, relheight=1, relwidth=0.105)

        self.btn_Tema = Button(
            self.master,
            text="TEMA",
            bg="gray90",
            fg='black',
            font=("Arial bold", 10),
            image=self.img_Tema,
            compound="top",
            command=lambda: self.tema(),
        )
        self.btn_Tema.place(relx=0.77, rely=0, relheight=1, relwidth=0.105)

        self.btn_Salir = Button(
            self.master,
            text="SALIR",
            bg="gray90",
            fg='black',
            font=("Arial bold", 10),
            image=self.img_Salir,
            compound="top",
            command=lambda: self.root.destroy(),
        )
        self.btn_Salir.place(relx=0.88, rely=0, relheight=1, relwidth=0.105)

    # PRUEBA DE COMANDOS
    def acciones(self, txt):
        print(txt)

    # CREAMOS EL TREEVIEW DONDE VAN A IR LOS RESULTADOS DE LA BUSQUEDA
    def crear_Treeview(self, srely=0.45, srelheight=0.5):
                
        self.listado = Frame(self.root, bg='papaya whip')
        self.listado.place(relx=0.01, rely=srely, relheight=srelheight, relwidth=0.99)
        scrollbar_y = Scrollbar(self.listado)
        scrollbar_y.place(relx=0.975, rely=0.01, relheight=0.99, relwidth=0.015)
        scrollbar_x = Scrollbar(self.listado)
        scrollbar_x.place(relx=0, rely=0.95, relheight=0.05, relwidth=0.975)

        # TREEVIEW
        self.tree = ttk.Treeview(
            self.listado,
            columns=("#1", "#2", "#3", "#4", "#5"),
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            selectmode="browse",
        )

        self.tree.place(relx=0, rely=0.01, relheight=0.95, relwidth=0.975)
        self.tree.heading("#0", text="ID")
        self.tree.heading("#1", text="NOMBRE")
        self.tree.heading("#2", text="RAZA")
        self.tree.heading("#3", text="VACUNAS")
        self.tree.heading("#4", text="TIPO")
        self.tree.heading("#5", text="FECHA")
        self.tree.column("#0", width=20)
        self.tree.column("#1", width=130)
        self.tree.column("#2", width=130)
        self.tree.column("#3", width=130)
        self.tree.column("#4", width=100)
        self.tree.column("#5", width=160)

        scrollbar_y.config(orient=VERTICAL, command=self.tree.yview)
        scrollbar_x.config(orient=HORIZONTAL, command=self.tree.xview)

    def crear_Menu(self):
        self.barraMenu = Menu(self.root)
        self.root.config(menu=self.barraMenu, width=300, height=300)

        self.fileMenu = Menu(self.barraMenu, tearoff=0)
        self.fileMenu.add_command(label="Salir", command=self.root.destroy)

        self.bdatosMenu = Menu(self.barraMenu, tearoff=0)
        self.bdatosMenu.add_command(
            label="Crear Nueva BD"
        )
        self.bdatosMenu.add_command(
            label="Crear Nueva Tabla"
        )

        self.helpMenu = Menu(self.barraMenu, tearoff=0)
        self.helpMenu.add_command(label="Acerca de...", command=self.ayuda)

        self.barraMenu.add_cascade(label="Archivo", menu=self.fileMenu)
        self.barraMenu.add_cascade(label="Base de Datos", menu=self.bdatosMenu)
        self.barraMenu.add_cascade(label="Ayuda", menu=self.helpMenu)

    def ayuda(self):
        """ Muestra ventanita de  acerda de """

        top_acerca = Toplevel(self.master)
        top_acerca.title("Mascotas Soft")
        top_acerca.iconphoto(True, PhotoImage(file="src/perro.png"))
        top_acerca.resizable(0, 0)

        acercaCanva = Canvas(
            top_acerca, 
            width=320, 
            height=250, 
            bg="black", 
            bd=0
        )
        acercaCanva.config(highlightbackground="black")
        acercaCanva.pack()

        acercaCanva.create_text(
            160, 30, 
            text="MASCOTAS", 
            font="Calibri 25 bold", 
            fill="white"
        )

        acercaCanva.create_text(
            160,
            120,
            text="Copyright  2020 Grupo III Python\n\nBROCHERO FRANCO\nKOVACIC MARTIN\nPICARD SMITH JUAN MARCOS\nSCILLATO GERMAN",
            font="Arial 12",
            fill="white",
        )
        acercaCanva.create_text(
            160, 
            200, 
            text="Version 4.0 a1", 
            font="Arial 12", 
            fill="white"
        )
        
        # METODOS PARA MANTENER EL FOCO EN EL TOPLEVEL 
        top_acerca.grab_set()
        top_acerca.focus_set()
        top_acerca.wait_window()
        #-------------------------------------------#

        top_acerca.mainloop()

    def tema(self, **kwargs):

        """ Modificar el tema de colores """
        if len(kwargs) == 0:

            self.result = askcolor(color="#00ff00", title="Seleccionar Color")

            try:
                # GUARDAMOS EL TEMA ELEGIDO EN UN ARCHIVO color.conf
                self.archivo_escritura = open("color.conf", "w+")
                self.archivo_escritura.write(str(self.result[1]))
                self.archivo_escritura.close()
                
                self.root.configure(background=str(self.result[1]))
                self.master.configure(background=str(self.result[1]))
                self.listado.configure(background=str(self.result[1]))
                # self.main_Frame.configure(background=str(self.result[1]))
                # self.label_Nombre.configure(background=str(self.result[1]))
                # self.label_Tipo.configure(background=str(self.result[1]))
                # self.label_Vacunas.configure(background=str(self.result[1]))
                # self.label_Raza.configure(background=str(self.result[1]))

            except:            
                return

        else:
            try:
                self.config_color = open("color.conf", "r")

                self.result = [0, self.config_color.read()]

                self.root.configure(background=str(self.result[1]))
                self.master.configure(background=str(self.result[1]))
                self.listado.configure(background=str(self.result[1]))
                # self.main_Frame.configure(background=str(self.result[1]))
                # self.label_Nombre.configure(background=str(self.result[1]))
                # self.label_Tipo.configure(background=str(self.result[1]))
                # self.label_Vacunas.configure(background=str(self.result[1]))
                # self.label_Raza.configure(background=str(self.result[1]))

            except:
                return

    def ver_todos(self):
        logica_App.ver_todos(self)

    def crear_Frame(self, **kwargs):

        self.main_Frame = Frame(self.root)
        self.main_Frame.place(relx=0.01, rely=0.19, relheight=0.25, relwidth=0.98)
        self.main_Frame.config(bg="papaya whip",borderwidth=2, relief='raised')

        # DAMOS UN TITULO AL FORMULARIO
        self.label_Titulo = Label(
            self.main_Frame,
            fg="green",
            text=kwargs['titulo'],
            font=("calibri bold", 15),
            bg= "gray80",
        )

        # CREAMOS LAS ETIQUETAS QUE INDICARAN QUE DATO INTRODUCIR EN CADA ENTRADA (ENTRY)

        self.label_Nombre = Label(
            self.main_Frame, 
            text="NOMBRE:", 
            font=("calibri bold", 11), 
            fg='black',
            bg="papaya whip"
            )

        self.label_Raza = Label(self.main_Frame, 
            text="RAZA:", 
            font=("calibri bold", 11), 
            fg='black',
            bg="papaya whip"
            )


        self.label_Vacunas = Label(
            self.main_Frame, 
            text="VACUNAS:", 
            font=("calibri bold", 11), 
            fg='black',
            bg="papaya whip"
            )

        self.label_Tipo = Label(self.main_Frame, 
            text="TIPO:", 
            font=("calibri bold", 11), 
            fg='black',
            bg="papaya whip"
            )

        # DEFINIMOS LAS VARIABLES QUE USAREMOS EN ESTE CASO 5
        self.nombre_var, self.raza_var, self.vacunas_var, self.tipo_var = (
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
        )

        # DEFINIMOS LOS CAMPOS DE ENTRADA "ENTRY"
        # self.entry_Editar = Entry(self.main_Frame, width=100, textvariable=self.id_edicion_var)
        self.entry_Nombre = Entry(self.main_Frame, width=100, textvariable=self.nombre_var)
        self.entry_Raza = Entry(self.main_Frame, width=100, textvariable=self.raza_var)
        self.entry_Vacunas = Entry(self.main_Frame, width=100, textvariable=self.vacunas_var)
        self.combo_Tipo = ttk.Combobox(self.main_Frame, width=50, state="readonly", textvariable=self.tipo_var)
        self.combo_Tipo["values"] = self.tipo_animal
        # UBICA LOS ELEMENTOS MEDIANTE EL SISTEMA DE GRILLA CON EL METODO GRID

        # TITULO
        self.label_Titulo.grid(row=0, column=0, columnspan=3, sticky=W + E)

        # ETIQUETAS
        # self.label_Editar.grid(row=1, column=0, sticky=W, padx=10, pady=1)
        self.label_Nombre.grid(row=2, column=0, sticky=W, padx=10, pady=1)
        self.label_Raza.grid(row=3, column=0, sticky=W, padx=10, pady=1)
        self.label_Vacunas.grid(row=4, column=0, sticky=W, padx=10, pady=1)
        self.label_Tipo.grid(row=5, column=0, sticky=W, padx=10, pady=1)

        # CAMPOS DE ENTRADA
        # self.entry_Editar.grid(row=1, column=1, padx=1, pady=1)
        self.entry_Nombre.grid(row=2, column=1, padx=1, pady=1)
        self.entry_Raza.grid(row=3, column=1, padx=1, pady=1)
        self.entry_Vacunas.grid(row=4, column=1, padx=1, pady=1)
        self.combo_Tipo.grid(row=5, column=1, padx=1, pady=1, sticky=W+E)

        # --------------  CREAMOS EL BOTON GUARDAR Y CANCELAR  -----------------------

        self.boton_Multiuso = Button(
            self.main_Frame,
            text=kwargs['boton'],
            font=("calibri bold", 11),
            width=30,
            command=kwargs['comando'],
        )
        self.boton_Multiuso.grid(row=6, column=1, sticky=E)

        self.boton_Cancelar = Button(
            self.main_Frame,
            text="CANCELAR",
            font=("calibri bold", 11),
            width=30,
            command=lambda :self.cierre_Frame(),
        )
        self.boton_Cancelar.grid(row=6, column=1,sticky=W)

        # ----------------   DESHABILITADO DE BOTONES   ------------------
        
        self.btn_Buscar.configure(state='disable')
        self.btn_Editar.configure(state='disable')
        self.btn_Nuevo.configure(state='disable')
        self.btn_Editar.configure(state='disable')
        
    def cierre_Frame(self):
        self.btn_Nuevo.configure(state='normal')
        self.btn_Buscar.configure(state='normal')
        self.btn_Eliminar.configure(state='normal')
        self.btn_Editar.configure(state='normal')
        self.main_Frame.destroy()

    def editar(self):
        self.crear_Frame(titulo='SELECCIONE UN REGISTRO PARA EDITAR', boton='EDITAR', comando=lambda:logica_App.Editar(self))

    def buscar(self):
        self.crear_Frame(titulo='BUSCAR', boton='BUSCAR', comando=lambda:logica_App.buscar_datos(self))

    def nuevo(self):
        self.crear_Frame(titulo='NUEVO REGISTRO', boton='GUARDAR', comando=lambda:logica_App.Guardar(self))    

    def eliminar(self):
        logica_App.eliminar_registro(self)

    def vacia_base_datos(self):
        """ Reinicia la base de datos """
        valor = messagebox.askquestion(
            "Restarurar", "Esta seguro de que desea borrar todos los datos?"
        )
        if valor == "yes":
            bd = CrudSqlite()
            bd.crear_tabla(self)
            self.limpiar()

    def _blank_form(self):
        """ Genera un form con los datos en blanco dentro del mainFrame """

        self.infoLbl.config(text="", fg="blue", font=("", 11, "bold"), bd=0)
        self._vacia_form()
        # CREAMOS LAS ETIQUETAS QUE INDICARAN QUE DATO INTRODUCIR EN CADA ENTRADA (ENTRY)
        l_nombre = Label(
            self.mainFrame,
            text="NOMBRE",
            font=("", 11, "bold"),
            fg="black",
            bg="papaya whip",
        )
        l_raza = Label(
            self.mainFrame,
            text="RAZA",
            font=("", 11, "bold"),
            fg="black",
            bg="papaya whip",
        )
        l_vacunas = Label(
            self.mainFrame,
            text="VACUNAS",
            font=("", 11, "bold"),
            fg="black",
            bg="papaya whip",
        )
        l_tipo = Label(
            self.mainFrame,
            text="TIPO",
            font=("", 11, "bold"),
            fg="black",
            bg="papaya whip",
        )

        l_nombre.grid(column=0, row=0, padx=4, pady=4, sticky="W")
        l_raza.grid(column=0, row=1, padx=4, pady=4, sticky="W")
        l_vacunas.grid(column=0, row=2, padx=4, pady=4, sticky="W")
        l_tipo.grid(column=0, row=3, padx=4, pady=4, sticky="W")

        # CRAMOS LOS ENTRY PARA LOS DATOS
        nombre = Entry(self.mainFrame, width=50)
        raza = Entry(self.mainFrame, width=50)
        vacunas = Entry(self.mainFrame, width=50)
        tipo = ttk.Combobox(self.mainFrame, width=50, state="readonly")
        tipo["values"] = self.tipo_animal
        nombre.grid(row=0, column=1, padx=1, pady=1, sticky="WE")
        nombre.name = "nombre"
        raza.grid(row=1, column=1, padx=1, pady=1, sticky="WE")
        raza.name = "raza"
        vacunas.grid(row=2, column=1, padx=1, pady=1, sticky="WE")
        vacunas.name = "vacunas"
        tipo.grid(row=3, column=1, padx=1, pady=1, sticky="WE")
        tipo.name = "tipo"

    def limpiar(self):
        self.tree.delete(*self.tree.get_children())
        #self.borrar_form()

    #def borrar_form(self):
       # self.nombre_var.set('')
       # self.raza_var.set('')
       # self.vacunas_var.set('')
       # self.tipo_var.set('')
    #    pass

# PROBANDO .....
if __name__ == "__main__":
    root = Tk()
    root.config(bg="papaya whip")
    root.state("zoomed")
    root.minsize(800, 600)
    root.iconphoto(False, PhotoImage(file="src/huellas.png"))
    root.title("MASCOTAS SOFT 3.0")
    gui(root)
    root.mainloop()
