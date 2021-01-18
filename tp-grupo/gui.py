import tkinter
import re

from tkinter import  ttk,messagebox
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk

import crud_sqlite
from multibox import MultiListbox

class CrudTk(tkinter.Frame):
    ''' Extiende la clase Frame de tk para poder manejar los contenedores y contenidos del crud '''

    def __init__(self, master):
        tkinter.Frame.__init__(self, master,height=300, width=100)
        
        self.tipo_animal = ["FELINO", "CANINO", "REPTIL", "AVE", "INSECTO", "PEZ"]
        
        # coneccion a la base de datos
        self.db = crud_sqlite.CrudSqlite()
        
        self.barraMenu = tkinter.Menu(master)
        master.config(menu=self.barraMenu, width=300, height=300)

        self.fileMenu = tkinter.Menu(self.barraMenu, tearoff=0)
        self.fileMenu.add_command(label="Salir", command=master.destroy)

        self.bdatosMenu = tkinter.Menu(self.barraMenu, tearoff=0)
        self.bdatosMenu.add_command(label="Crear Nueva BD", command=self.vacia_base_datos)
        self.bdatosMenu.add_command(label="Crear Nueva Tabla", command=self.vacia_base_datos )
        #self.bdatosMenu.add_command(label="Crear Nuevo Registro",command=self.nuevo_registro)
        #self.bdatosMenu.add_separator()
        #self.bdatosMenu.add_command(label="Ver Todos los Regitros",)
        #self.bdatosMenu.add_separator()
        #self.bdatosMenu.add_command(label="Eliminar BD",)
        #self.bdatosMenu.add_command(label="Eliminar Tabla",)
        #self.bdatosMenu.add_command(label="Eliminar Registro",)

        self.helpMenu = tkinter.Menu(self.barraMenu, tearoff=0)
        self.helpMenu.add_command(label="Acerca de...", command = self.ayuda)

        self.barraMenu.add_cascade(label="Archivo", menu=self.fileMenu)
        self.barraMenu.add_cascade(label="Base de Datos", menu=self.bdatosMenu)
        self.barraMenu.add_cascade(label="Ayuda", menu=self.helpMenu)
        
        self.botonera = tkinter.LabelFrame(master, bg="papaya whip", bd=0, height=100)
        self.botonera.pack(fill="x", padx=2,pady=2,side='top')
       
        # CREAMOS UN FRAME DONDE PONDERMOS LOS COMPONENTES A USAR EN CADA MOMENTO 
        self.mainFrame = tkinter.LabelFrame(master,bg='papaya whip', bd=1)
        self.mainFrame.pack(fill="both", padx=2,pady=2, expand='y', side='top')
        
        # CREAMOS UN FRAME INFERIOR PARA EL INFO
        self.infoFrame = tkinter.LabelFrame(master, bg="black", bd=1, height=100)
        self.infoFrame.pack(side="bottom", fill="x")
        self.infoLbl = tkinter.Label(self.infoFrame, text="", font=( '', 11, 'bold'),fg='white',bg='black')
        self.infoLbl.grid(column=0, row=0, padx=4, pady=4, sticky='W')

        # DEFINIMOS LA IMAGEN A USAR EN EL BOTON NUEVO Y LO DEFINIMOS
        # COMO NO VAMOS A USARLO MAS ADELANTE. NO DEFINIMOS UNA VARIABLE QUE APUNTE AL OBJETO
        # EL CAMBIO DE TEMA ES SOLO PARA CAMBIAR EL COLOR DE FONDO DE LA APP.
        # USAMOS PLACE PARA QUE LA APP SE ADAPTE A LA RESOLUCION QUE TENGA DISPONIBLE O PREFIERA EL USUARIO
        self.img = ImageTk.PhotoImage(Image.open("img/019-add.png"))
        tkinter.Button(
            self.botonera,
            text="NUEVO",
            bg="gray90",
            font=("Arial bold", 10),
            fg='black',
            image=self.img,
            compound="top",
            command=self.nuevo_registro,
        ).place(relx=0, rely=0, relheight=1, relwidth=0.105)

        # DEFINIMOS LA IMAGEN A USAR EN EL BOTON EDITAR Y LO DEFINIMOS
        self.img2 = ImageTk.PhotoImage(Image.open("img/018-edit.png"))
        self.btn_editar = tkinter.Button(
            self.botonera,
            text="EDITAR",
            bg="gray90",
            font=("Arial bold", 10),
            fg='black',
            image=self.img2,
            compound="top",
            state="disabled",
            #command=editar,
        )
        self.btn_editar.place(relx=0.11, rely=0, relheight=1, relwidth=0.105)

        # DEFINIMOS LA IMAGEN A USAR EN EL BOTON ELIMINAR Y LO DEFINIMOS
        self.img3 = ImageTk.PhotoImage(Image.open("img/015-remove.png"))
        self.btn_eliminar = tkinter.Button(
            self.botonera,
            text="ELIMINAR",
            bg="gray90",
            font=("Arial bold", 10),
            fg='black',
            image=self.img3,
            compound="top",
            state="disabled",
            command=self.eliminar_registro,
        )
        self.btn_eliminar.place(relx=0.22, rely=0, relheight=1, relwidth=0.105)

        # DEFINIMOS LA IMAGEN A USAR EN EL BOTON ELIMINAR Y LO DEFINIMOS
        self.img4 = ImageTk.PhotoImage(Image.open("img/027-search.png"))
        tkinter.Button(
            self.botonera,
            text="BUSCAR",
            bg="gray90",
            font=("Arial bold", 10),
            fg='black',
            image=self.img4,
            compound="top",
            command=self.buscar_datos,
        ).place(relx=0.33, rely=0, relheight=1, relwidth=0.105)

        # DEFINIMOS LA IMAGEN A USAR EN EL BOTON VER TODO Y LO DEFINIMOS
        self.img5 = ImageTk.PhotoImage(Image.open("img/005-infographic.png"))
        tkinter.Button(
            self.botonera,
            text="VER TODO",
            bg="gray90",
            font=("Arial bold", 10),
            fg='black',
            image=self.img5,
            compound="top",
            #command=ver_registros,
        ).place(relx=0.44, rely=0, relheight=1, relwidth=0.105)

        # DEFINIMOS LA IMAGEN A USAR EN EL BOTON LIMPIAR Y LO DEFINIMOS        
        self.img6 = ImageTk.PhotoImage(Image.open("img/023-remove.png"))
        tkinter.Button(
            self.botonera,
            text="LIMPIAR",
            bg="gray90",
            font=("Arial bold", 10),
            fg='black',
            image=self.img6,
            compound="top",
            command=self.vacia_base_datos,
        ).place(relx=0.55, rely=0, relheight=1, relwidth=0.105)

        # DEFINIMOS LA IMAGEN A USAR EN EL BOTON RESTAURAR Y LO DEFINIMOS
        self.img7 = ImageTk.PhotoImage(Image.open("img/024-reload.png"))
        tkinter.Button(
            self.botonera,
            text="RESTAURAR",
            bg="gray90",
            font=("Arial bold", 10),
            fg='black',
            image=self.img7,
            compound="top",
            command=self.vacia_base_datos,
        ).place(relx=0.66, rely=0, relheight=1, relwidth=0.105)

        # DEFINIMOS LA IMAGEN A USAR EN EL BOTON TEMA Y LO DEFINIMOS
        self.img8 = ImageTk.PhotoImage(Image.open("img/028-setting.png"))
        tkinter.Button(
            self.botonera,
            text="TEMA",
            bg="gray90",
            font=("Arial bold", 10),
            fg='black',
            image=self.img8,
            compound="top",
            command=self.tema,
        ).place(relx=0.77, rely=0, relheight=1, relwidth=0.105)       
        
        # DEFINIMOS LA IMAGEN A USAR EN EL BOTON SALIR Y LO DEFINIMOS        
        self.img9 = ImageTk.PhotoImage(Image.open("img/icon_cancelar.png"))
        tkinter.Button(
            self.botonera,
            text="SALIR",
            bg="gray90",
            font=("Arial bold", 10),
            fg='black',
            image=self.img9,
            compound="top",
            command=master.destroy,
        ).place(relx=0.88, rely=0, relheight=1, relwidth=0.105)

    def vacia_base_datos(self):
        ''' Reinicia la base de datos '''
        valor = messagebox.askquestion("Restarurar","Esta seguro de que desea borrar todos los datos?")
        if valor == "yes":
            self.db.nueva_tabla()


    def eliminar_registro(self):
        ''' Elimina un el registro seleccionado del listbox '''
        r = self.Lb1.__getitem__(self.Lb1.curselection()) 
        valor = messagebox.askquestion("Eliminar","Esta seguro de eliminar el registro seleccionado?")
        if valor == "yes":
            # ELIMINA EL REGISTRO SELECCIONADO EN EL GRID       
            self.db.elimina_datos({'id':r[0]})
        try:
            self._buscar_datos()
        except:
            pass

    def tema(self):
        ''' Modificar el tema de colores '''
        result = askcolor(color="#00ff00", title="Seleccionar Color")

        try:
            self.master.configure(background=str(result[1]))
            #listado.configure(background=str(result[1]))
            self.botonera.configure(background=str(result[1]))
            self.mainFrame.configure(background=str(result[1]))
        except:
            return

    def _vacia_form(self):
        ''' destruye los elementos del form '''        
        # ELIMINA TODOS LOS WIDGETS DEL MAINFRAME PARA PODER USARLO DE NUEVO
        self.mainFrame.config(text="", bd=0)
        for cosa in self.mainFrame.winfo_children():
            cosa.destroy()
        self.btn_editar.configure(state="disable")
        self.btn_eliminar.configure(state="disable")


    def _blank_form(self):
        ''' Genera un form con los datos en blanco dentro del mainFrame '''

        self.infoLbl.config(text="",fg="blue", font=( '', 11, 'bold'), bd=0)        
        self._vacia_form()             
        # CREAMOS LAS ETIQUETAS QUE INDICARAN QUE DATO INTRODUCIR EN CADA ENTRADA (ENTRY)
        l_nombre = tkinter.Label(self.mainFrame, text="NOMBRE", font=( '', 11, 'bold'),fg='black',bg='papaya whip')
        l_raza = tkinter.Label(self.mainFrame, text="RAZA", font=( '', 11, 'bold'),fg='black',bg='papaya whip')
        l_vacunas = tkinter.Label(self.mainFrame, text="VACUNAS", font=( '', 11, 'bold'),fg='black',bg='papaya whip')
        l_tipo = tkinter.Label(self.mainFrame, text="TIPO", font=( '', 11, 'bold'),fg='black',bg='papaya whip')

        l_nombre.grid(column=0, row=0, padx=4, pady=4, sticky='W')
        l_raza.grid(column=0, row=1, padx=4, pady=4, sticky='W')
        l_vacunas.grid(column=0, row=2, padx=4, pady=4, sticky='W')
        l_tipo.grid(column=0, row=3, padx=4, pady=4, sticky='W')
        
        # CRAMOS LOS ENTRY PARA LOS DATOS
        nombre = tkinter.Entry(self.mainFrame, width=50)        
        raza = tkinter.Entry(self.mainFrame, width=50)
        vacunas = tkinter.Entry(self.mainFrame, width=50)
        tipo = ttk.Combobox(self.mainFrame, width=50, state="readonly")    
        tipo["values"] = self.tipo_animal
        nombre.grid(row=0, column=1, padx=1, pady=1,sticky="WE")
        nombre.name='nombre'
        raza.grid(row=1, column=1, padx=1, pady=1,sticky="WE")
        raza.name='raza'
        vacunas.grid(row=2, column=1, padx=1, pady=1,sticky="WE")
        vacunas.name='vacunas'
        tipo.grid(row=3, column=1, padx=1, pady=1,sticky="WE")
        tipo.name='tipo'

    def buscar_datos(self):
        ''' Busca en la base de datos en base a lo ingresado en el form '''

        self._blank_form()
        self.mainFrame.config(text="Buscar ingreso",fg="blue", font=( '', 13, 'bold'), bd=1)

        # LABEL VACIO PARA SEPARAR LOS BOTONES DE LOS ENTRY        
        lfake = tkinter.Label(self.mainFrame, text="", font=( '', 11, 'bold'),bg='papaya whip', width='10')
        lfake.grid(column=2, row=0, padx=4, pady=4, sticky='nswe')

        b_alta = tkinter.Button(
            self.mainFrame, text="BUSCAR",  font=( '', 11, ''),width='10',
            command=self._buscar_datos
        )
        b_alta.grid(row=0,column=3,padx=1, pady=1,sticky='WS')

        # CREAMOS EL FRAME DONDE VAN A IR LOS RESULTADOS DE LA BUSQUDA
        listado = tkinter.Frame(self.mainFrame, bg="papaya whip")
        listado.place(relx=0.01, rely=0.3, relheight=0.68, relwidth=0.99)
        self.Lb1 = MultiListbox(listado, ['Id', 'Nombre', 'Raza','Vacunas','Tipo','Fecha'], width=4)        
        self.Lb1.pack(fill="both", expand=True)


    def _buscar_datos(self):
        r = {}
        # RECORREMOS LOS WIDGET DEL MAINFRAME PARA OBTENER LOS ENTRY DE DATOS
        for h in self.mainFrame.winfo_children():
            if isinstance(h,tkinter.Entry):
                if len(h.get()) != 0:
                    # COMPROBAMOS QUE SE INGRESEN SOLO CARACTERES ALFANUMERICOS
                    if re.fullmatch("^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$",h.get()) is None:
                        self.infoLbl.config(text="Solo permiten caracteres alfanumericos ("+h.name+")",fg="red", font=( '', 11, 'bold'), bd=0)
                        return
                    r[h.name] = h.get()
        # VACIAMOS EL GRID
        self.Lb1.vaciar()
        try :
            result = self.db.busca_datos(r)
            # LO LLENAMOS CON LOS RESULTADOS
            for r in result:
                self.Lb1.add_data(r)
        except:
            self.infoLbl.config(text="No se ha podido realizar la busqueda ",fg="red", font=( '', 11, 'bold'), bd=0)
        
        if len(r) > 0 :
            self.btn_editar.configure(state="normal")
            self.btn_eliminar.configure(state="normal")

    def nuevo_registro(self):
        ''' Arma el form para un nuevo registro''' 
        
        # CONFIGURAMOS EL MAINFRAME PARA UN NUEVO INGRESO
        self._blank_form()
        self.mainFrame.config(text="Nuevo ingreso",fg="blue", font=( '', 13, 'bold'), bd=1)

        lfake = tkinter.Label(self.mainFrame, text="", font=( '', 11, 'bold'),bg='papaya whip', width='10')
        lfake.grid(column=2, row=0, padx=4, pady=4, sticky='nswe')
        
        # AGREGAMOS LOS BOTONES PARA GUARDAR O CANCELAR
        b_alta = tkinter.Button(
            self.mainFrame, text="GUARDAR",  font=( '', 11, ''),width='10',
            command=self._guardar_datos
        )
        b_alta.grid(row=0,column=3,padx=1, pady=1,sticky='WS')
        
        b_cancel = tkinter.Button(
            self.mainFrame, text="CANCELAR",  font=( '', 11, ''),width='10',            
            command=self._vacia_form
        )
        b_cancel.grid(row=2,column=3, padx=1, pady=1,sticky='ES')
        self.update()

    def _guardar_datos(self):        
        r = {}
        for h in self.mainFrame.winfo_children():
            if isinstance(h,tkinter.Entry):
                if len(h.get()) == 0:
                    # COMPRUEBA QUE NO SE INGRESEN CAMPOS VACIOS
                    self.infoLbl.config(text="No se permiten campos vacios ("+h.name+")",fg="red", font=( '', 11, 'bold'), bd=0)
                    return
                if re.fullmatch("^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$",h.get()) is None:
                    # COMPRUEBA QUE SOLO SE INGRESEN CARACTERES ALFANUMERICOS
                    self.infoLbl.config(text="Solo permiten caracteres alfanumericos ("+h.name+")",fg="red", font=( '', 11, 'bold'), bd=0)
                    return
                r[h.name] = h.get()
        try:
            self.db.guarda_datos(r)
            self.infoLbl.config(text="Ultimo registro guardado correctamente",fg="white", font=( '', 11, 'bold'), bd=0)
        except:
            self.infoLbl.config(text="No se ha podido guardar el registro",fg="red", font=( '', 11, 'bold'), bd=0)
        self._vacia_form()

    def ayuda(self):
        ''' Muestra ventanita de  acerda de '''

        top_acerca = tkinter.Toplevel(self.master)
        top_acerca.title("Mascotas Soft")
        top_acerca.iconphoto(True, tkinter.PhotoImage(file="img/perro.png"))
        top_acerca.resizable(0, 0)

        acercaCanva = tkinter.Canvas(top_acerca, width=320, height=250, bg="black", bd=0)
        acercaCanva.config(highlightbackground="black")
        acercaCanva.pack()
        acercaCanva.create_text(
            160, 30, text="MASCOTAS", font="Calibri 25 bold", fill="white"
        )

        acercaCanva.create_text(
            160,
            120,
            text="Copyright  2020 Grupo III Python\n\nBROCHERO FRANCO\nKOVACIC MARTIN\nPICARD SMITH JUAN MARCOS\nSCILLATO GERMAN",
            font="Arial 12",
            fill="white",
        )
        acercaCanva.create_text(160, 200, text="Version 4.0 a1", font="Arial 12", fill="white")
        top_acerca.grab_set()
        top_acerca.focus_set()
        top_acerca.wait_window()

        top_acerca.mainloop()
