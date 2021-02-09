import tkinter
import re
import datetime
from tkinter import ttk
from tkinter import messagebox
from modelo import CrudSqlite

class logica_App:

    def __init__(self):
        self.tipo_animal = ["FELINO", "CANINO", "REPTIL", "AVE", "INSECTO", "PEZ"]
        # coneccion a la base de datos
        self.db = CrudSqlite()

    def vacia_base_datos(self):
        """ Reinicia la base de datos """
        valor = messagebox.askquestion(
            "Restarurar", "Esta seguro de que desea borrar todos los datos?"
        )
        if valor == "yes":
            self.db.nueva_tabla()

    def eliminar_registro(self):
        """ Elimina un el registro seleccionado del Treeview """
        #  TRAE DEL GRID EL ID DEL ANIMAL
        try: 
            item_id = self.tree.item(self.tree.selection()[0], option="text")

            valor = messagebox.askquestion(
                "Eliminar", 
                "Esta seguro de eliminar el registro seleccionado?"
            )

            if valor == "yes":
                # ELIMINA EL REGISTRO SELECCIONADO EN EL GRID
                db = CrudSqlite()
                db.elimina_datos({"id": item_id})
                #self.borrar_form()
        except:
            self.infoLbl.configure(text='NO HAY DATOS SELECCIONADOS')

    def _vacia_form(self):
        """ destruye los elementos del form """
        # ELIMINA TODOS LOS WIDGETS DEL MAINFRAME PARA PODER USARLO DE NUEVO
        self.root.config(text="", bd=0)
        for cosa in self.mainFrame.winfo_children():
            cosa.destroy()
        self.btn_editar.configure(state="disable")
        self.btn_eliminar.configure(state="disable")

    def _blank_form(self):
        """ Genera un form con los datos en blanco dentro del mainFrame """

        self.infoLbl.config(text="", fg="blue", font=("", 11, "bold"), bd=0)
        self._vacia_form()
        # CREAMOS LAS ETIQUETAS QUE INDICARAN QUE DATO INTRODUCIR EN CADA ENTRADA (ENTRY)
        l_nombre = tkinter.Label(
            self.mainFrame,
            text="NOMBRE",
            font=("", 11, "bold"),
            fg="black",
            bg="papaya whip",
        )
        l_raza = tkinter.Label(
            self.mainFrame,
            text="RAZA",
            font=("", 11, "bold"),
            fg="black",
            bg="papaya whip",
        )
        l_vacunas = tkinter.Label(
            self.mainFrame,
            text="VACUNAS",
            font=("", 11, "bold"),
            fg="black",
            bg="papaya whip",
        )
        l_tipo = tkinter.Label(
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
        nombre = tkinter.Entry(self.mainFrame, width=50)
        raza = tkinter.Entry(self.mainFrame, width=50)
        vacunas = tkinter.Entry(self.mainFrame, width=50)
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

    def _nuevo_grid(self, srely=0.3, srelheight=0.68):
        # CREAMOS EL FRAME DONDE VAN A IR LOS RESULTADOS DE LA BUSQUDA
        listado = tkinter.Frame(self.main_Frame, bg="papaya whip")
        listado.place(relx=0.01, rely=srely, relheight=srelheight, relwidth=0.99)
        scrollbar_y = tkinter.Scrollbar(listado)
        scrollbar_y.place(relx=0.975, rely=0.01, relheight=0.99, relwidth=0.015)
        scrollbar_x = tkinter.Scrollbar(listado)
        scrollbar_x.place(relx=0, rely=0.95, relheight=0.05, relwidth=0.975)

        # TREEVIEW
        self.tree = ttk.Treeview(
            listado,
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

        scrollbar_y.config(orient=tkinter.VERTICAL, command=self.tree.yview)
        scrollbar_x.config(orient=tkinter.HORIZONTAL, command=self.tree.xview)

    def buscar_datos(self):
        r = {}
        # RECORREMOS LOS WIDGET DEL MAINFRAME PARA OBTENER LOS ENTRY DE DATOS
        r['nombre'] = self.nombre_var.get()
        r['raza'] = self.raza_var.get()
        r['vacunas'] = self.vacunas_var.get()
        r['tipo'] = self.tipo_var.get()
        
        self.db = CrudSqlite()
        result = self.db.busca_datos(r)

        self.tree.delete(*self.tree.get_children())

        try:
        
            for r in result:
                    fecha_animal = datetime.datetime.strptime(r[-1], "%y-%m-%d %H:%M:%S")
                    r = list(r)
                    r[-1] = fecha_animal.strftime("%d/%m/%Y %H:%M:%S")

            self.tree.insert(
                        "",
                        1,
                        text=r[0],
                        values=r[1:],
                    )
        except:
            self.infoLbl.configure(
                text="No se ha podido realizar la busqueda ",
                fg="red",
                font=("", 11, "bold"),
                bd=0,
            )

    def nuevo_registro(self):
        """ Arma el form para un nuevo registro"""

        # CONFIGURAMOS EL MAINFRAME PARA UN NUEVO INGRESO
        self._blank_form()
        self.mainFrame.config(
            text="Nuevo ingreso", fg="blue", font=("", 13, "bold"), bd=1
        )

        lfake = tkinter.Label(
            self.mainFrame, text="", font=("", 11, "bold"), bg="papaya whip", width="10"
        )
        lfake.grid(column=2, row=0, padx=4, pady=4, sticky="nswe")

        # AGREGAMOS LOS BOTONES PARA GUARDAR O CANCELAR
        b_alta = tkinter.Button(
            self.mainFrame,
            text="GUARDAR",
            font=("", 11, ""),
            width="10",
            command=self._guardar_datos,
        )
        b_alta.grid(row=0, column=3, padx=1, pady=1, sticky="WS")

        b_cancel = tkinter.Button(
            self.mainFrame,
            text="CANCELAR",
            font=("", 11, ""),
            width="10",
            command=self._vacia_form,
        )
        b_cancel.grid(row=2, column=3, padx=1, pady=1, sticky="ES")
        self.update()

    def ver_todos(self):

        self.limpiar()
        """ Mostrar todos los registros en el grid """
        # self._vacia_form()
        try:
            self.db = CrudSqlite()
            result = self.db.busca_datos({"tipo": "%"})
            # self._nuevo_grid(srely=0, srelheight=0.99)
            for r in result:
                fecha_animal = datetime.datetime.strptime(r[-1], "%y-%m-%d %H:%M:%S")
                r = list(r)
                r[-1] = fecha_animal.strftime("%d/%m/%Y %H:%M:%S")
                self.tree.insert(
                    "",
                    1,
                    text=r[0],
                    values=r[1:],
                )
        except:
            self.infoLbl.config(
                text="No se ha podido realizar la busqueda ",
                fg="red",
                font=("", 11, "bold"),
                bd=0,
            )

    def _guardar_datos(self):
        r = {}
        for h in self.mainFrame.winfo_children():
            if isinstance(h, tkinter.Entry):
                if len(h.get()) == 0:
                    # COMPRUEBA QUE NO SE INGRESEN CAMPOS VACIOS
                    self.infoLbl.config(
                        text="No se permiten campos vacios (" + h.name + ")",
                        fg="red",
                        font=("", 11, "bold"),
                        bd=0,
                    )
                    return
                if (
                    re.fullmatch("^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$", h.get())
                    is None
                ):
                    # COMPRUEBA QUE SOLO SE INGRESEN CARACTERES ALFANUMERICOS
                    self.infoLbl.config(
                        text="Solo permiten caracteres alfanumericos (" + h.name + ")",
                        fg="red",
                        font=("", 11, "bold"),
                        bd=0,
                    )
                    return
                r[h.name] = h.get()
        try:
            self.db.guarda_datos(r)
            self.infoLbl.config(
                text="Ultimo registro guardado correctamente",
                fg="white",
                font=("", 11, "bold"),
                bd=0,
            )
        except:
            self.infoLbl.config(
                text="No se ha podido guardar el registro",
                fg="red",
                font=("", 11, "bold"),
                bd=0,
            )
        self._vacia_form()

    def Guardar(self):
        if (
            len(
                self.nombre_var.get()
                and self.raza_var.get()
                and self.vacunas_var.get()
                and self.tipo_var.get()
            )
            != 0
        ):            

            registro = {
                'nombre' : self.nombre_var.get(),
                'raza' : self.raza_var.get(),
                'vacunas' : self.vacunas_var.get(),
                'tipo' : self.tipo_var.get(),
            }

            CrudSqlite().nuevo_Registro(registro)

            self.infoLbl.configure(text='GUARDADO EXITOSAMENTE')
            print ( "gurda")
            #self.borrar_form()
            self.ver_todos()


        else:
            self.infoLbl.configure(text='OCURRIO UN ERROR - NO SE PERMITEN CAMPOS VACIOS')

    def Editar(self):
        registro = {
                'nombre' : self.nombre_var.get(),
                'raza' : self.raza_var.get(),
                'vacunas' : self.vacunas_var.get(),
                'tipo' : self.tipo_var.get(),
            }
        
        self.db = CrudSqlite()

        """ update del registro seleccionado del Treeview """

        #  TRAE DEL GRID EL ID DEL ANIMAL
        item_id = self.tree.item(self.tree.selection()[0], option="text")
        registro["id"] = item_id

        # EDITA EL REGISTRO SELECCIONADO EN EL GRID
        db = CrudSqlite()
        db.edita_datos(registro)
        self.ver_todos()
        self.infoLbl.configure(text='DATOS EDITADOS CORRECTAMENTE')