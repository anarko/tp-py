#Library import
import tkinter
import datetime
from tkinter import  ttk,messagebox
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
#Local import
import crud_sqlite
from validator import StrVarConValidador
from refugio_v4 import APP_PATH


class CrudTk(tkinter.Frame):
    """ Extiende la clase Frame de tk para poder manejar los contenedores y contenidos del crud """

    def __init__(self, master):
        tkinter.Frame.__init__(self, master,height=300, width=100)
        
        self.tipo_animal = ["FELINO", "CANINO", "REPTIL", "AVE", "INSECTO", "PEZ"]
        
        # coneccion a la base de datos
        self.db = crud_sqlite.CrudSqlite(APP_PATH+"/refugio.db")
        
        self.barraMenu = tkinter.Menu(master)
        master.config(menu=self.barraMenu, width=300, height=300)

        self.fileMenu = tkinter.Menu(self.barraMenu, tearoff=0)
        self.fileMenu.add_command(label="Salir", command=master.destroy)

        self.bdatosMenu = tkinter.Menu(self.barraMenu, tearoff=0)
        self.bdatosMenu.add_command(label="Crear Nueva BD", command=self.vacia_base_datos)
        self.bdatosMenu.add_command(label="Crear Nueva Tabla", command=self.vacia_base_datos )

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
        self.default_bg = "papaya whip"
        # DEFINIMOS LA IMAGEN A USAR EN EL BOTON NUEVO Y LO DEFINIMOS
        # COMO NO VAMOS A USARLO MAS ADELANTE. NO DEFINIMOS UNA VARIABLE QUE APUNTE AL OBJETO
        # EL CAMBIO DE TEMA ES SOLO PARA CAMBIAR EL COLOR DE FONDO DE LA APP.
        # USAMOS PLACE PARA QUE LA APP SE ADAPTE A LA RESOLUCION QUE TENGA DISPONIBLE O PREFIERA EL USUARIO
        self.img = ImageTk.PhotoImage(Image.open(APP_PATH+"/img/019-add.png"))
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
        self.img2 = ImageTk.PhotoImage(Image.open(APP_PATH+"/img/018-edit.png"))
        self.btn_editar = tkinter.Button(
            self.botonera,
            text="EDITAR",
            bg="gray90",
            font=("Arial bold", 10),
            fg='black',
            image=self.img2,
            compound="top",
            state="disabled",
            command=self._editar_datos_seleccionados,
        )
        self.btn_editar.place(relx=0.11, rely=0, relheight=1, relwidth=0.105)

        # DEFINIMOS LA IMAGEN A USAR EN EL BOTON ELIMINAR Y LO DEFINIMOS
        self.img3 = ImageTk.PhotoImage(Image.open(APP_PATH+"/img/015-remove.png"))
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
        self.img4 = ImageTk.PhotoImage(Image.open(APP_PATH+"/img/027-search.png"))
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
        self.img5 = ImageTk.PhotoImage(Image.open(APP_PATH+"/img/005-infographic.png"))
        tkinter.Button(
            self.botonera,
            text="VER TODO",
            bg="gray90",
            font=("Arial bold", 10),
            fg='black',
            image=self.img5,
            compound="top",
            command=self.ver_todos,
        ).place(relx=0.44, rely=0, relheight=1, relwidth=0.105)

        # DEFINIMOS LA IMAGEN A USAR EN EL BOTON LIMPIAR Y LO DEFINIMOS        
        self.img6 = ImageTk.PhotoImage(Image.open(APP_PATH+"/img/023-remove.png"))
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
        self.img7 = ImageTk.PhotoImage(Image.open(APP_PATH+"/img/024-reload.png"))
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
        self.img8 = ImageTk.PhotoImage(Image.open(APP_PATH+"/img/028-setting.png"))
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
        self.img9 = ImageTk.PhotoImage(Image.open(APP_PATH+"/img/icon_cancelar.png"))
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

        self.nombre_var, self.raza_var, self.vacunas_var, self.tipo_var = (
            StrVarConValidador(),
            StrVarConValidador(),
            StrVarConValidador(),
            StrVarConValidador(),
        )

    def vacia_base_datos(self):
        """ Reinicia la base de datos """
        
        valor = messagebox.askquestion("Restarurar","Esta seguro de que desea borrar todos los datos?")
        if valor == "yes":
            self.db.nueva_tabla()

    def eliminar_registro(self):
        """ Elimina un el registro seleccionado del listbox """

        #  TRAE DEL GRID EL ID DEL ANIMAL
        try:
            item_id = self.tree.item(self.tree.selection()[0],option="text")        
            valor = messagebox.askquestion("Eliminar","Esta seguro de eliminar el registro seleccionado?")
            if valor == "yes":
                # ELIMINA EL REGISTRO SELECCIONADO EN EL GRID       
                self.db.elimina_datos({'id':item_id})
        except:
            self.infoLbl.config(text="Debe seleccionar un elemento para eliminar",fg="red", font=( '', 11, 'bold'), bd=0)
            
        self.ver_todos()

    def tema(self):
        """ Modificar el tema de colores """

        result = askcolor(color="#00ff00", title="Seleccionar Color")

        try:
            self.master.configure(background=str(result[1]))
            self.botonera.configure(background=str(result[1]))
            self.mainFrame.configure(background=str(result[1]))
            self.default_bg = str(result[1])
        except:
            pass

    def _vacia_form(self):
        """ Destruye los elementos del form """

        # ELIMINA TODOS LOS WIDGETS DEL MAINFRAME PARA PODER USARLO DE NUEVO
        self.mainFrame.config(text="", bd=0)
        for cosa in self.mainFrame.winfo_children():
            cosa.destroy()
        self.btn_editar.configure(state="disable")
        self.btn_eliminar.configure(state="disable")

    def _editar_datos_seleccionados(self):
        """ Abre el form para editar los datos de un registro """

        #  TRAE DEL GRID EL ID DEL ANIMAL
        hay_elemento_seleciconado = False
        try:
            item_id = self.tree.item(self.tree.selection()[0],option="text")        
            hay_elemento_seleciconado = True
        except:
            self.infoLbl.config(text="Debe seleccionar un elemento para editar",fg="red", font=( '', 11, 'bold'), bd=0)
            
        if hay_elemento_seleciconado is True:
            self._blank_form()
            result = self.db.busca_datos({"id":item_id})[0]
            self.mainFrame.config(text="Mofificar",fg="blue", font=( '', 13, 'bold'), bd=1)
            
            # asigno los valores a modificar
            self.nombre_var.set(result[1])
            self.raza_var.set(result[2])
            self.vacunas_var.set(result[3])
            self.tipo_var.set(result[4])
            
            lfake = tkinter.Label(self.mainFrame, text="", font=( '', 11, 'bold'),bg=self.default_bg, width='10')
            lfake.grid(column=2, row=0, padx=4, pady=4, sticky='nswe')
            
            # AGREGAMOS LOS BOTONES PARA GUARDAR O CANCELAR
            b_alta = tkinter.Button(
                self.mainFrame, text="GUARDAR",  font=( '', 11, ''),width='10',
                command =   lambda : self._guardar_datos(item_id)
            )
            b_alta.grid(row=0,column=3,padx=1, pady=1,sticky='WS')
            
            b_cancel = tkinter.Button(
                self.mainFrame, text="CANCELAR",  font=( '', 11, ''),width='10',            
                command=self._vacia_form
            )
            b_cancel.grid(row=2,column=3, padx=1, pady=1,sticky='ES')
            self.update()

    def _blank_form(self):
        """ Genera un form con los datos en blanco dentro del mainFrame """

        self.infoLbl.config(text="",fg="blue", font=( '', 11, 'bold'), bd=0)        
        self._vacia_form()             
        # CREAMOS LAS ETIQUETAS QUE INDICARAN QUE DATO INTRODUCIR EN CADA ENTRADA (ENTRY)
        l_nombre = tkinter.Label(self.mainFrame, text="NOMBRE", font=( '', 11, 'bold'),fg='black',bg=self.default_bg)
        l_raza = tkinter.Label(self.mainFrame, text="RAZA", font=( '', 11, 'bold'),fg='black',bg=self.default_bg)
        l_vacunas = tkinter.Label(self.mainFrame, text="VACUNAS", font=( '', 11, 'bold'),fg='black',bg=self.default_bg)
        l_tipo = tkinter.Label(self.mainFrame, text="TIPO", font=( '', 11, 'bold'),fg='black',bg=self.default_bg)

        l_nombre.grid(column=0, row=0, padx=4, pady=4, sticky='W')
        l_raza.grid(column=0, row=1, padx=4, pady=4, sticky='W')
        l_vacunas.grid(column=0, row=2, padx=4, pady=4, sticky='W')
        l_tipo.grid(column=0, row=3, padx=4, pady=4, sticky='W')
        
        self.nombre_var.set('')
        self.raza_var.set('')
        self.vacunas_var.set('')
        self.tipo_var.set('')

        # CRAMOS LOS ENTRY PARA LOS DATOS
        nombre = tkinter.Entry(self.mainFrame, width=50, textvariable=self.nombre_var)
        raza = tkinter.Entry(self.mainFrame, width=50, textvariable=self.raza_var)
        vacunas = tkinter.Entry(self.mainFrame, width=50, textvariable=self.vacunas_var)
        tipo = ttk.Combobox(self.mainFrame, width=50, state="readonly", textvariable=self.tipo_var)    
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
        """ Busca en la base de datos en base a lo ingresado en el form """

        self._blank_form()
        self.mainFrame.config(text="Buscar ingreso",fg="blue", font=( '', 13, 'bold'), bd=1)

        # LABEL VACIO PARA SEPARAR LOS BOTONES DE LOS ENTRY        
        lfake = tkinter.Label(self.mainFrame, text="", font=( '', 11, 'bold'),bg=self.default_bg, width='10')
        lfake.grid(column=2, row=0, padx=4, pady=4, sticky='nswe')

        b_alta = tkinter.Button(
            self.mainFrame, text="BUSCAR",  font=( '', 11, ''),width='10',
            command=self._buscar_datos
        )
        b_alta.grid(row=0,column=3,padx=1, pady=1,sticky='WS')
        self._nuevo_grid()
        
    def _nuevo_grid(self, srely=0.3,srelheight=0.68):
        """ Crea un grid en blanco para mostrar los resultados """

        # CREAMOS EL FRAME DONDE VAN A IR LOS RESULTADOS DE LA BUSQUDA
        listado = tkinter.Frame(self.mainFrame, bg=self.default_bg)
        listado.place(relx=0.01, rely=srely, relheight=srelheight, relwidth=0.99)
        scrollbar_y = tkinter.Scrollbar(listado)
        scrollbar_y.place(relx=0.975, rely=0.01, relheight=0.99, relwidth=0.015)
        scrollbar_x = tkinter.Scrollbar(listado)
        scrollbar_x.place(relx=0, rely=0.95, relheight=0.05, relwidth=0.975)

        # TREEVIEW
        self.tree = ttk.Treeview(
            listado,
            columns=("#1", "#2", "#3", "#4","#5"),
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

        scrollbar_y.config(orient=tkinter.VERTICAL, command=self.tree.yview)
        scrollbar_x.config(orient=tkinter.HORIZONTAL, command=self.tree.xview)

    def _buscar_datos(self):
        """ Busca en la base de datos de acuerdo con los entry completos en el form 
            si no pusieron caracteres alfanumericos en los entry no los considera para la busqueda
        """

        r = {}
        if self.nombre_var.validar_no_vacio() :
            if self.nombre_var.validar_alfanumerico() is False:
                self.infoLbl.config(text="Solo permiten caracteres alfanumericos en el nombre",fg="red", font=( '', 11, 'bold'), bd=0)
            else:
                r['nombre'] = self.nombre_var.get()

        if self.raza_var.validar_no_vacio() :
            if self.raza_var.validar_alfanumerico() is False:
                self.infoLbl.config(text="Solo permiten caracteres alfanumericos en la raza",fg="red", font=( '', 11, 'bold'), bd=0)
            else:
                r['raza'] = self.raza_var.get()

        if self.vacunas_var.validar_no_vacio() :
            if self.vacunas_var.validar_alfanumerico() is False:
                self.infoLbl.config(text="Solo permiten caracteres alfanumericos para las vacunas",fg="red", font=( '', 11, 'bold'), bd=0)
            else:
                r['vacunas'] = self.vacunas_var.get()

        if self.tipo_var.validar_no_vacio() :
            if self.tipo_var.validar_alfanumerico() is False:
                self.infoLbl.config(text="Solo permiten caracteres alfanumericos para el tipo",fg="red", font=( '', 11, 'bold'), bd=0)
            else:
                r['tipo'] = self.tipo_var.get()

        # VACIAMOS EL GRID
        self.tree.delete(*self.tree.get_children())
        try :
            result = self.db.busca_datos(r)
            # LO LLENAMOS CON LOS RESULTADOS
            for r in result:
                fecha_animal = datetime.datetime.strptime(r[-1], '%y-%m-%d %H:%M:%S')
                r = list(r)
                r[-1] = fecha_animal.strftime("%d/%m/%Y %H:%M:%S")

                self.tree.insert(
                "",
                1,
                text=r[0],
                values=r[1:],
                )
        except:
            self.infoLbl.config(text="No se ha podido realizar la busqueda ",fg="red", font=( '', 11, 'bold'), bd=0)
        
        if len(r) > 0 :
            self.btn_editar.configure(state="normal")
            self.btn_eliminar.configure(state="normal")

    def nuevo_registro(self):
        """ Arma el form para un nuevo registro""" 
        
        # CONFIGURAMOS EL MAINFRAME PARA UN NUEVO INGRESO
        self._blank_form()
        self.mainFrame.config(text="Nuevo ingreso",fg="blue", font=( '', 13, 'bold'), bd=1)

        lfake = tkinter.Label(self.mainFrame, text="", font=( '', 11, 'bold'),bg=self.default_bg, width='10')
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

    def ver_todos(self):
        """ Mostrar todos los registros en el grid """ 

        try:
            result = self.db.busca_datos({"tipo":"%"})
            self._nuevo_grid(srely=0,srelheight=0.99)            
            for r in result:
                fecha_animal = datetime.datetime.strptime(r[-1], '%y-%m-%d %H:%M:%S')
                r = list(r)
                r[-1] = fecha_animal.strftime("%d/%m/%Y %H:%M:%S")
                self.tree.insert(
                "",
                1,
                text=r[0],
                values=r[1:],
                )

            if len(r) > 0 :
                self.btn_editar.configure(state="normal")
                self.btn_eliminar.configure(state="normal")                

        except:
            self.infoLbl.config(text="No se ha podido realizar la busqueda ",fg="red", font=( '', 11, 'bold'), bd=0)    

    def _guardar_datos(self,item_id = None):
        """ Guarda los datos en base a los datos ingresados en los entry
            si recibe un id es una modificacion, sino es un registro nuevo
        """
        
        campos_validos = True
        r = {}

        if ( self.nombre_var.validar_alfanumerico() is False or self.nombre_var.validar_no_vacio() is False 
            or self.raza_var.validar_alfanumerico() is False or self.raza_var.validar_no_vacio() is False 
            or self.vacunas_var.validar_alfanumerico() is False or self.vacunas_var.validar_no_vacio() is False
            or self.tipo_var.validar_alfanumerico() is False or self.tipo_var.validar_no_vacio() is False ):
                campos_validos = False

        if campos_validos is True:
            try:
                r['nombre'] = self.nombre_var.get()
                r['raza'] = self.raza_var.get()
                r['vacunas'] = self.vacunas_var.get()
                r['tipo'] = self.tipo_var.get()
                if item_id is not None:
                    r['id'] = item_id
                self.db.guarda_datos(r)
                self.infoLbl.config(text="Ultimo registro guardado correctamente",fg="white", font=( '', 11, 'bold'), bd=0)
                self._vacia_form()
            except:
                self.infoLbl.config(text="No se ha podido guardar el registro",fg="red", font=( '', 11, 'bold'), bd=0)
        else:
            self.infoLbl.config(text="Solo se permiten caracteres alfanumercos en los datos",fg="red", font=( '', 11, 'bold'), bd=0)

    def ayuda(self):
        """ Muestra ventanita de  acerda de """

        top_acerca = tkinter.Toplevel(self.master)
        top_acerca.title("Mascotas Soft")
        top_acerca.iconphoto(True, tkinter.PhotoImage(file=APP_PATH+"/img/perro.png"))
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
