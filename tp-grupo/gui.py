import tkinter
from tkinter import  ttk,messagebox
import re
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk

import crud_sqlite

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
        self.bdatosMenu.add_command(label="Crear Nueva BD", command=self.db.nueva_tabla)
        self.bdatosMenu.add_command(label="Crear Nueva Tabla", command=self.db.nueva_tabla )
        self.bdatosMenu.add_command(label="Crear Nuevo Registro",command=self.nuevo_registro)
        self.bdatosMenu.add_separator()
        self.bdatosMenu.add_command(label="Ver Todos los Regitros",)
        self.bdatosMenu.add_separator()
        self.bdatosMenu.add_command(label="Eliminar BD",)
        self.bdatosMenu.add_command(label="Eliminar Tabla",)
        self.bdatosMenu.add_command(label="Eliminar Registro",)

        self.helpMenu = tkinter.Menu(self.barraMenu, tearoff=0)
        self.helpMenu.add_command(label="Acerca de...", command = self.ayuda)

        self.barraMenu.add_cascade(label="Archivo", menu=self.fileMenu)
        self.barraMenu.add_cascade(label="Base de Datos", menu=self.bdatosMenu)
        self.barraMenu.add_cascade(label="Ayuda", menu=self.helpMenu)
        
        self.botonera = tkinter.LabelFrame(master, bg="papaya whip", bd=0, height=100)
        self.botonera.pack(fill="x", padx=2,pady=2,side='top')

        #self.botonera.place(relx=0.01, rely=0.01, relheight=0.17, relwidth=0.98)
        
        #self.botonera.pack( side = tkinter.BOTTOM )
        #self.botonera = tkinter. LabelFrame(self, text="This is a LabelFrame")
        
        self.mainFrame = tkinter.LabelFrame(master,bg='papaya whip', bd=1)
        self.mainFrame.pack(fill="both", padx=2,pady=2, expand='y', side='top')

        
        self.infoFrame = tkinter.LabelFrame(master, bg="black", bd=1, height=100)
        self.infoFrame.pack(side="bottom", fill="x")
        self.infoLbl = tkinter.Label(self.infoFrame, text="", font=( '', 11, 'bold'),fg='white',bg='black')
        self.infoLbl.grid(column=0, row=0, padx=4, pady=4, sticky='W')


      # self.mainFrame = tkinter.Frame(master, bg="green")
      #  self.mainFrame.place(relx=0.01, rely=0.01, relheight=0.17, relwidth=0.98)        

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
        tkinter.Button(
            self.botonera,
            text="EDITAR",
            bg="gray90",
            font=("Arial bold", 10),
            fg='black',
            image=self.img2,
            compound="top",
            #command=editar,
        ).place(relx=0.11, rely=0, relheight=1, relwidth=0.105)

        # DEFINIMOS LA IMAGEN A USAR EN EL BOTON ELIMINAR Y LO DEFINIMOS
        self.img3 = ImageTk.PhotoImage(Image.open("img/015-remove.png"))
        tkinter.Button(
            self.botonera,
            text="ELIMINAR",
            bg="gray90",
            font=("Arial bold", 10),
            fg='black',
            image=self.img3,
            compound="top",
            #command=eliminar_registro,
        ).place(relx=0.22, rely=0, relheight=1, relwidth=0.105)

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
            #command=buscar,
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
            #command=limpiar,
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
            #command=restaurar,
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
    


    def tema(self):
        result = askcolor(color="#00ff00", title="Seleccionar Color")

        try:
            self.master.configure(background=str(result[1]))
            #listado.configure(background=str(result[1]))
            self.botonera.configure(background=str(result[1]))
        except:
            return

    def _vacia_form(self):
        ''' destruye los elementos del form '''        
        self.mainFrame.config(text="", bd=0)
        for cosa in self.mainFrame.winfo_children():
            cosa.destroy()
        self.infoLbl.config(text="",fg="blue", font=( '', 11, 'bold'), bd=0)

    def nuevo_registro(self):
        
        self._vacia_form()     
        self.mainFrame.config(text="Nuevo ingreso",fg="blue", font=( '', 13, 'bold'), bd=1)
        
        # CREAMOS LAS ETIQUETAS QUE INDICARAN QUE DATO INTRODUCIR EN CADA ENTRADA (ENTRY)
        l_nombre = tkinter.Label(self.mainFrame, text="NOMBRE", font=( '', 11, 'bold'),fg='black',bg='papaya whip')
        l_raza = tkinter.Label(self.mainFrame, text="RAZA", font=( '', 11, 'bold'),fg='black',bg='papaya whip')
        l_vacunas = tkinter.Label(self.mainFrame, text="VACUNAS", font=( '', 11, 'bold'),fg='black',bg='papaya whip')
        l_tipo = tkinter.Label(self.mainFrame, text="TIPO", font=( '', 11, 'bold'),fg='black',bg='papaya whip')

        l_nombre.grid(column=0, row=0, padx=4, pady=4, sticky='W')
        l_raza.grid(column=0, row=1, padx=4, pady=4, sticky='W')
        l_vacunas.grid(column=0, row=2, padx=4, pady=4, sticky='W')
        l_tipo.grid(column=0, row=3, padx=4, pady=4, sticky='W')
        
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

        lfake = tkinter.Label(self.mainFrame, text="", font=( '', 11, 'bold'),bg='papaya whip', width='10')
        lfake.grid(column=2, row=0, padx=4, pady=4, sticky='nswe')

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

        '''
        self.top_buscar = tkinter.Toplevel(self.master)
        self.top_buscar.iconphoto(True, tkinter.PhotoImage(file="img/perro.png"))
        self.top_buscar.resizable(0, 0)
        self.top_buscar.title("NUEVO REGISTRO")

        self.top_buscar.config(bg="gray80")
        # DAMOS UN TITULO AL FORMULARIO
        l_titulo = tkinter.Label(
            self.top_buscar,
            fg="white",
            text="ALTA DE MASCOTAS",
            font=("calibri bold", 15),
        )
                        
        
        

        
        # CREAMOS LAS ETIQUETAS QUE INDICARAN QUE DATO INTRODUCIR EN CADA ENTRADA (ENTRY)
        l_nombre = tkinter.Label(self.top_buscar, text="NOMBRE", font=("calibri bold", 11), bg="gray80")
        l_raza = tkinter.Label(self.top_buscar, text="RAZA", font=("calibri bold", 11), bg="gray80")
        l_vacunas = tkinter.Label(
            self.top_buscar, text="VACUNAS", font=("calibri bold", 11), bg="gray80"
        )
        l_tipo = tkinter.Label(self.top_buscar, text="TIPO", font=("calibri bold", 11), bg="gray80")

        # DEFINIMOS LOS CAMPOS DE ENTRADA "ENTRY"
        nombre = tkinter.Entry(self.top_buscar, width=50)
        raza = tkinter.Entry(self.top_buscar, width=50)
        vacunas = tkinter.Entry(self.top_buscar, width=50)
        #tipo = Entry(top_buscar, width=100, textvariable=tipo_var)
        tipo = ttk.Combobox(self.top_buscar, width=50, state="readonly")    
        tipo["values"] = self.tipo_animal
        
        # UBICA LOS ELEMENTOS MEDIANTE EL SISTEMA DE GRILLA CON EL METODO GRID

        # TITULO
        l_titulo.grid(row=0, column=0, columnspan=3, sticky=tkinter.W + tkinter.E)
        l_titulo.config(bg="steel blue")  # Ponemos color de fondo al titulo

        # ETIQUETAS
        l_nombre.grid(row=2, column=0, sticky=tkinter.W, padx=10, pady=1)
        l_raza.grid(row=3, column=0, sticky=tkinter.W, padx=10, pady=1)
        l_vacunas.grid(row=4, column=0, sticky=tkinter.W, padx=10, pady=1)
        l_tipo.grid(row=5, column=0, sticky=tkinter.W, padx=10, pady=1)

        # CAMPOS DE ENTRADA
        nombre.grid(row=2, column=1, padx=1, pady=1, columnspan=2)
        nombre.name='nombre'
        raza.grid(row=3, column=1, padx=1, pady=1, columnspan=2)
        raza.name='raza'
        vacunas.grid(row=4, column=1, padx=1, pady=1, columnspan=2)
        vacunas.name='vacunas'
        tipo.grid(row=5, column=1, padx=1, pady=1, columnspan=2)
        tipo.name='tipo'

        color_sorpresa = "gray80"

        self.top_buscar.configure(background=color_sorpresa)
        l_nombre.configure(background=color_sorpresa)
        l_raza.configure(background=color_sorpresa)
        l_vacunas.configure(background=color_sorpresa)
        l_tipo.configure(background=color_sorpresa)

        # CREAMOS EL BOTON BUSCAR, DAMOS EL GRID

        b_alta = tkinter.Button(
            self.top_buscar, text="ALTA REGISTRO", font=("calibri bold", 11),              
            command=self._guardar_datos
        )
        b_alta.grid(row=6, column=1, padx=1, pady=1, sticky=tkinter.W + tkinter.E)
        b_cancel = tkinter.Button(
            self.top_buscar, text="CANCELAR", font=("calibri bold", 11),              
            command=lambda :self.top_buscar.destroy()
        )
        b_cancel.grid(row=6, column=2, padx=1, pady=1, sticky=tkinter.W + tkinter.E)

        nombre.focus_set()

        # METODOS PARA MANTENER LA PRIORIDAD DE TOPLEVEL SOBRE TK
        self.top_buscar.grab_set()
        self.top_buscar.focus_set()
        self.top_buscar.wait_window()
        self.top_buscar.mainloop()
        '''

    def _guardar_datos(self):        
        r = {}
        for h in self.mainFrame.winfo_children():
            if isinstance(h,tkinter.Entry):
                if len(h.get()) == 0:
                    self.infoLbl.config(text="No se permiten campos vacios ("+h.name+")",fg="red", font=( '', 11, 'bold'), bd=0)
                   # return messagebox.showwarning("ADVERTENCIA", "NO SE PERMITEN CAMPOS VACIOS")
                    return
                if re.fullmatch("^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$",h.get()) is None:
                    self.infoLbl.config(text="No se permiten caracteres alfanumericos ("+h.name+")",fg="red", font=( '', 11, 'bold'), bd=0)
                    return
                    #return messagebox.showwarning("ADVERTENCIA", "SOLO SE PERMITEN CARACTERES ALFANUMERICOS")
                r[h.name] = h.get()
        try:
            self.db.guarda_datos(r)
            self.infoLbl.config(text="Ultimo registro guardado correctamente",fg="blue", font=( '', 11, 'bold'), bd=0)
        except:
            self.infoLbl.config(text="No se ha podido guardar el registro",fg="red", font=( '', 11, 'bold'), bd=0)
        self._vacia_form()

    def ayuda(self):
        
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
            text="Copyright  2020 Grupo III Python\n\nBROCHERO FRANCO\nDIAZ VIVERA MICAELA\nKOVACIC MARTIN\nPICARD SMITH JUAN MARCOS\nSCILLATO GERMAN",
            font="Arial 12",
            fill="white",
        )
        acercaCanva.create_text(160, 200, text="Version 4.0 a1", font="Arial 12", fill="white")
        top_acerca.grab_set()
        top_acerca.focus_set()
        top_acerca.wait_window()

        top_acerca.mainloop()
