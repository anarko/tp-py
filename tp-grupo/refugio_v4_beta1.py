# ----------------------------------------------------IMPORTAMOS LO QUE USAREMOS ---------------------------------------------------------
from tkinter import (
    Button,
    Frame,
    Scrollbar,
    Tk,
    ttk,
    Menu,
    mainloop,
    Toplevel,
    Canvas,
    Label,
    StringVar,
    IntVar,
    Scrollbar,
    Entry,
    Listbox,
    messagebox,
    Radiobutton,
    PhotoImage,
)

from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
import datetime
from tkinter.constants import VERTICAL, HORIZONTAL, END, W, E, N, S
import re
import mysql.connector
from mysql.connector import Error
import sys,os

# ----------------------------------------------------DEFINIMOS LA VENTANA PRINCIPAL-------------------------------------------------
root = Tk()
root.config(bg="papaya whip")

root.state("normal")
root.minsize(800, 600)
root.iconphoto(False, PhotoImage(file="img/huellas.png"))
root.title("MASCOTAS SOFT 3.0")

# ----------------------------------------------------CREAMOS FUNCIONES PARA EL SOFT ------------------------------------------------
# ----------------------------------------------------FUNCION PARA NUEVO REGISTRO ---------------------------------------------------
inicio = 0


def conn():

    try:
        bd = mysql.connector.connect(
            host="localhost", user="anarko", passwd="marcos", database=""
        )
        return bd

    except Error as e:
        messagebox.showerror(("ERROR: " + str(e.errno)), e.msg)


def crear_bd(sql="CREATE DATABASE IF NOT EXISTS MASCOTAS"):

    try:

        bd = mysql.connector.connect(host="localhost", user="anarko", passwd="marcos")

        c = bd.cursor()

        c.execute(sql)

    except Error as e:
        messagebox.showerror(("ERROR: " + str(e.errno)), e.msg)

    if inicio == 1:
        messagebox.showinfo("CONEXION ESTABLECIDA", "BASE DE DATOS CREADA CON EXITO")


def crear_tabla(
    sql="""CREATE TABLE IF NOT EXISTS registro ( id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, nombre VARCHAR(128)  NOT NULL, 
        raza varchar(128) NOT NULL, vacunas varchar (128)NOT NULL, tipo varchar (128), fecha date, hora time )""",
):

    bd = conn()

    if bd is not None:

        c = bd.cursor()

        c.execute(sql)
        if inicio == 1:
            messagebox.showinfo("CONEXION ESTABLECIDA", "NUEVA TABLA CREADA CON EXITO")


# -------------------------------------------------INICIACION DE BD PRIMER USO / RESSTABLECER BD-------------------------------------------------------
def restaurar():

    msg = ""

    if inicio == 1:
        msg = messagebox.askokcancel(
            "Base de Datos",
            "ESTA ACCION REINICIA LA BASE DE DATOS, SE BORRARAN TODOS LOS REGISTROS",
        )

        if msg == True:

            try:
                bd = conn()

                c = bd.cursor()

                c.execute("DROP DATABASE MASCOTAS")

                crear_bd(sql="CREATE DATABASE MASCOTAS")

                crear_tabla(
                    sql="""CREATE TABLE REGISTRO ( id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, nombre VARCHAR(128)  NOT NULL, 
        raza varchar(128) NOT NULL, vacunas varchar (128)NOT NULL, tipo varchar (128), fecha date, hora time )"""
                )

            except:
                messagebox.showinfo("INFORMACION", "NO SE PUDO CREAR LA BASE DE DATOS")
        else:
            return
    else:
        try:
            crear_bd()
            crear_tabla()
        except:
            return


restaurar()
inicio = 1

# ............................................ALTA DE NUEVA MASCOTA QUE INGRESA AL REFUGIO.................................


def new_reg():
    def alta():
        tipo = ["FELINO", "CANINO", "REPTIL", "AVE", "INSECTO", "PEZ"]

        if (
            len(
                nombre_var.get()
                and raza_var.get()
                and vacunas_var.get()
                and tipo_var.get()
            )
            == 0
        ):
            return messagebox.showwarning("ADVERTENCIA", "NO SE PERMITEN CAMPOS VACIOS")

        # VALIDACION TIPO REGEX
        patron = re.compile(r"^[0-9]+$")

        if re.match(patron, str(tipo_var.get())):
            return messagebox.showwarning(
                "ADVERTENCIA", "EL CAMPO TIPO NO PUEDE CONTENER N LOS DE LA LISTAUMEROS"
            )

        # VALIDACION TIPO (FILTRADO SEGUN LISTA PREDEFINIDA)
        patron = re.compile(str("^" + tipo_var.get() + "$"), flags=re.IGNORECASE)
        check_tipo = list(filter(patron.match, tipo))
        if not check_tipo:
            return messagebox.showwarning("ADVERTENCIA", "VERIFICAR TIPO")

        bd = conn()

        c = bd.cursor()

        sql = "INSERT INTO registro (nombre, raza, vacunas, tipo, fecha, hora) VALUES (%s, %s, %s, %s, %s, %s)"

        fecha = datetime.datetime.now().strftime("%y-%m-%d")

        hora = datetime.datetime.now().strftime("%H:%M:%S")

        datos = (
            nombre_var.get(),
            raza_var.get(),
            vacunas_var.get(),
            tipo_var.get(),
            fecha,
            hora,
        )

        c.execute(sql, datos)

        bd.commit()

        if c.rowcount > 0:
            messagebox.showinfo(
                title="Mensaje",
                message=str(c.rowcount) + " Registro creado exitosamente",
            )
        else:
            messagebox.showinfo(title="Mensaje", message="No se pudo crear el registro")
        bd.close()

    top_buscar = Toplevel(root)
    top_buscar.iconphoto(True, PhotoImage(file="img/perro.png"))
    top_buscar.resizable(0, 0)
    top_buscar.title("NUEVO REGISTRO")

    top_buscar.config(bg="gray80")
    # DAMOS UN TITULO AL FORMULARIO
    l_titulo = Label(
        top_buscar,
        fg="white",
        text="ALTA DE MASCOTAS",
        font=("calibri bold", 15),
    )

    # CREAMOS LAS ETIQUETAS QUE INDICARAN QUE DATO INTRODUCIR EN CADA ENTRADA (ENTRY)
    l_nombre = Label(top_buscar, text="NOMBRE:", font=("calibri bold", 11), bg="gray80")
    l_raza = Label(top_buscar, text="RAZA:", font=("calibri bold", 11), bg="gray80")
    l_vacunas = Label(
        top_buscar, text="VACUNAS:", font=("calibri bold", 11), bg="gray80"
    )
    l_tipo = Label(top_buscar, text="TIPO:", font=("calibri bold", 11), bg="gray80")

    # DEFINIMOS LAS VARIABLES QUE USAREMOS EN ESTE CASO 3
    nombre_var, raza_var, vacunas_var, tipo_var = (
        StringVar(),
        StringVar(),
        StringVar(),
        StringVar(),
    )

    # DEFINIMOS LOS CAMPOS DE ENTRADA "ENTRY"
    nombre = Entry(top_buscar, width=100, textvariable=nombre_var)
    raza = Entry(top_buscar, width=100, textvariable=raza_var)
    vacunas = Entry(top_buscar, width=100, textvariable=vacunas_var)
    #tipo = Entry(top_buscar, width=100, textvariable=tipo_var)
    tipo = ttk.Combobox(top_buscar, width=100)    
    tipo["values"] = ["FELINO", "CANINO", "REPTIL", "AVE", "INSECTO", "PEZ"]
    
    # UBICA LOS ELEMENTOS MEDIANTE EL SISTEMA DE GRILLA CON EL METODO GRID

    # TITULO
    l_titulo.grid(row=0, column=0, columnspan=2, sticky=W + E)
    l_titulo.config(bg="steel blue")  # Ponemos color de fondo al titulo

    # ETIQUETAS
    l_nombre.grid(row=2, column=0, sticky=W, padx=10, pady=1)
    l_raza.grid(row=3, column=0, sticky=W, padx=10, pady=1)
    l_vacunas.grid(row=4, column=0, sticky=W, padx=10, pady=1)
    l_tipo.grid(row=5, column=0, sticky=W, padx=10, pady=1)

    # CAMPOS DE ENTRADA
    nombre.grid(row=2, column=1, padx=1, pady=1)
    raza.grid(row=3, column=1, padx=1, pady=1)
    vacunas.grid(row=4, column=1, padx=1, pady=1)
    tipo.grid(row=5, column=1, padx=1, pady=1)

    color_sorpresa = "gray80"

    top_buscar.configure(background=color_sorpresa)
    l_nombre.configure(background=color_sorpresa)
    l_raza.configure(background=color_sorpresa)
    l_vacunas.configure(background=color_sorpresa)
    l_tipo.configure(background=color_sorpresa)

    # CREAMOS EL BOTON BUSCAR, DAMOS EL GRID

    b_bucar = Button(
        top_buscar, text="ALTA REGISTRO", font=("calibri bold", 11), command=alta
    )
    b_bucar.grid(row=6, column=1, padx=1, pady=1, sticky=W + E)

    nombre.focus_set()

    # METODOS PARA MANTENER LA PRIORIDAD DE TOPLEVEL SOBRE TK
    top_buscar.grab_set()
    top_buscar.focus_set()
    top_buscar.wait_window()

    top_buscar.mainloop()


# ----------------------------------------------------FUNCION PARA ACERCA DE DEL MENU AYUDA CON CANVAS--------------------------------------------------


def ayuda():

    top_acerca = Toplevel(root)
    top_acerca.title("Mascotas Soft")
    top_acerca.iconphoto(True, PhotoImage(file="img/perro.png"))
    top_acerca.resizable(0, 0)

    acercaCanva = Canvas(top_acerca, width=320, height=250, bg="black", bd=0)
    acercaCanva.config(highlightbackground="black")
    acercaCanva.pack()
    acercaCanva.create_text(
        160, 30, text="MASCOTAS", font="Calibri 25 bold", fill="white"
    )

    acercaCanva.create_text(
        160,
        120,
        text="Copyright  2020 Grupo III Python\n\nBROCHERO FRANCO\nDIAZ VIVERA MICAELA\nKOVACIC MARTIN\nSCILLATO GERMAN",
        font="Arial 12",
        fill="white",
    )
    acercaCanva.create_text(160, 200, text="Version 3.0", font="Arial 12", fill="white")
    top_acerca.grab_set()
    top_acerca.focus_set()
    top_acerca.wait_window()

    top_acerca.mainloop()


# -------------------------------------- SE PREGUNTA EN CASO DE ACCION INVOLUNTARIA PARA QUE NO SE BORRE NADA-----------------------------------------


def eliminator(texto1, sql_sentence):
    bd = conn()
    c = bd.cursor()
    valor = messagebox.askquestion("ESTA ACCION BORRARA TODOS LOS DATOS", texto1)
    if valor == "yes":
        c.execute(sql_sentence)


# --------------------------------------------------------ELIMINAR BD-----------------------------------------------------------------------


def eliminar_bd():
    bd = conn()
    eliminator(" ESTA SEGURO DE ELIMINAR LA BASE DE DATOS ?", "DROP DATABASE MASCOTAS")
    bd.commit()
    bd.close()


# -------------------------------------------------ELIMINAR TABLA--------------------------------------------------------------------


def eliminar_tabla():
    bd = conn()
    eliminator(" ESTA SEGURO DE ELIMINAR LA TABLA ?", "DROP TABLE REGISTRO")
    bd.commit()
    bd.close()


# -------------------------------------------------ELIMINAR REGISTRO-----------------------------------------------------------------


def eliminar_registro():
    def logica_eliminar():

        # USAMOS TRY PARA CAPTURAR LAS EXCEPCIONES EN CASO DE ERROR

        try:

            bd = conn()

            c = bd.cursor()

            if opcion.get() == 1:
                sql = "DELETE FROM REGISTRO WHERE NOMBRE = '%s'" % (eliminar_var.get())

            elif opcion.get() == 2:
                sql = "DELETE FROM REGISTRO WHERE RAZA = '%s'" % (eliminar_var.get())

            else:
                sql = "DELETE FROM REGISTRO WHERE ID = %s" % (eliminar_var.get())

            c.execute(sql)

            bd.commit()

            if c.rowcount > 0:
                messagebox.showinfo(
                    title="Mensaje",
                    message=str(c.rowcount) + " El registro fue eliminado",
                )
            else:
                messagebox.showinfo(
                    title="Mensaje",
                    message="No se pudo eliminar el registro o no existe",
                )

            bd.close()

            eliminar.delete(0, END)

        except:
            messagebox.showinfo("INFORMACION", "NO SE COMPLETO LA OPERACION")

    top_eliminar = Toplevel(root)
    top_eliminar.iconphoto(True, PhotoImage(file="img/perro.png"))
    top_eliminar.resizable(0, 0)
    top_eliminar.title("ELIMINAR REGISTRO")
    top_eliminar.iconphoto(False, PhotoImage(file="img/huellas.png"))
    top_eliminar.config(bg="gray80")

    # DAMOS UN TITULO AL FORMULARIO
    l_titulo = Label(
        top_eliminar,
        fg="white",
        text="ELIMINAR REGISTRO",
        font=("calibri bold", 15),
        bg="red",
    )

    # CREAMOS LA ETIQUETA QUE INDICARAN QUE DATO INTRODUCIR EN CADA ENTRADA (ENTRY)
    l_eliminar = Label(
        top_eliminar, text="ELIMINAR:", font=("calibri bold", 11), bg="gray80"
    )

    # DEFINIMOS LAS VARIABLES QUE USAREMOS EN ESTE CASO 2
    eliminar_var, opcion = StringVar(), IntVar()

    # DEFINIMOS EL CAMPO DE ENTRADA "ENTRY"

    eliminar = Entry(top_eliminar, width=100, textvariable=eliminar_var)

    # DEFINIMOS EL RADIOBUTTON PARA ELEGIR SOBRE QUE DATO HACER LA SECUENCIA SQL

    op_nombre = Radiobutton(
        top_eliminar,
        text="NOMBRE",
        variable=opcion,
        value=1,
        bg="gray80",
    )
    op_raza = Radiobutton(
        top_eliminar,
        text="RAZA",
        variable=opcion,
        value=2,
        bg="gray80",
    )
    op_id = Radiobutton(
        top_eliminar,
        text="ID",
        variable=opcion,
        value=3,
        bg="gray80",
    )

    # UBICA LOS ELEMENTOS MEDIANTE EL SISTEMA DE GRILLA CON EL METODO GRID

    # GRID DE TITULO
    l_titulo.grid(row=0, column=0, columnspan=2, sticky=W + E)

    # GRID ETIQUETAS
    l_eliminar.grid(row=2, column=0, sticky=W, padx=10, pady=15)

    # GRID RADIOBUTTON
    op_id.grid(row=1, column=1, sticky=W, padx=10, pady=1)
    op_raza.grid(row=1, column=1, sticky=W, padx=60, pady=1)
    op_nombre.grid(row=1, column=1, sticky=W, padx=110, pady=1)

    # GRID CAMPO DE ENTRADA ELIMINAR

    eliminar.grid(row=2, column=1, padx=1, pady=15)

    # CREAMOS EL BOTON DE ELIMINAR, DAMOS EL GRID
    b_eliminar = Button(
        top_eliminar,
        text="ELIMINAR REGISTRO",
        font=("calibri bold", 11),
        command=logica_eliminar,
    )
    b_eliminar.grid(row=6, column=1, padx=1, pady=1, sticky=W + E)

    top_eliminar.grab_set()
    top_eliminar.focus_set()
    top_eliminar.wait_window()

    top_eliminar.mainloop()


# -------------------------------------------------FN VER REGISTROS ----------------------------------------------------------------


def ver_registros():
    try:

        Lb1.delete(0, END)

        bd = conn()

        c = bd.cursor()

        sql = "SELECT * FROM REGISTRO "

        c.execute(sql)

        reg = c.fetchall()

        campos = [
            "ID: ",
            "  NOMBRE: ",
            "  RAZA: ",
            "  VACUNAS: ",
            "  TIPO: ",
            "  FECHA: ",
            "  HORA: ",
        ]

        for i, n, r, v, t, f, h in reg:
            Lb1.insert(
                0,
                (
                    campos[0]
                    + str(i)
                    + campos[1]
                    + str(n)
                    + campos[2]
                    + str(r)
                    + campos[3]
                    + str(v)
                    + campos[4]
                    + str(t)
                    + campos[5]
                    + str(f)
                    + campos[6]
                    + str(h)
                ),
            )

        bd.close()
    except:
        return


# -------------------------------------------------FN BUSCAR REGISTROS -------------------------------------------------------------


def buscar():
    def search():
        def logica_buscar(
            sql="SELECT * FROM REGISTRO WHERE ID = '%s'" % (id_busqueda_var.get()),
        ):

            Lb1.delete(0, END)

            bd = conn()

            c = bd.cursor()

            c.execute(sql)

            reg = c.fetchall()

            campos = [
                "ID: ",
                "  NOMBRE: ",
                "  RAZA: ",
                "  VACUNAS: ",
                "  TIPO: ",
                "  FECHA: ",
                "  HORA: ",
            ]

            for i, n, r, v, t, f, h in reg:
                Lb1.insert(
                    0,
                    (
                        campos[0]
                        + str(i)
                        + campos[1]
                        + str(n)
                        + campos[2]
                        + str(r)
                        + campos[3]
                        + str(v)
                        + campos[4]
                        + str(t)
                        + campos[5]
                        + str(f)
                        + campos[6]
                        + str(h)
                    ),
                )

            bd.close()

        # VALIDACIONES REGEX

        validacion_id = re.compile(r"[0-9]")
        validacion_nombre_raza = re.compile(r"[^0-9]")

        if re.match(validacion_id, str(id_busqueda_var.get())) and opcion.get() == 3:
            logica_buscar()

        elif (
            re.match(validacion_nombre_raza, str(id_busqueda_var.get()))
            and opcion.get() == 2
        ):

            logica_buscar(
                sql="SELECT * FROM REGISTRO WHERE RAZA = '%s'" % (id_busqueda_var.get())
            )

        elif (
            re.match(validacion_nombre_raza, str(id_busqueda_var.get()))
            and opcion.get() == 1
        ):

            logica_buscar(
                sql="SELECT * FROM REGISTRO WHERE NOMBRE = '%s'"
                % (id_busqueda_var.get())
            )

        else:

            return messagebox.showwarning(
                "ADVERTENCIA",
                "EL CAMPO BUSQUEDA DEBE CONTENER:\n--->NUMEROS PARA BUSCAR ID\n--->LETRAS PARA BUSCAR POR RAZA O NOMBRE",
            )

    top_buscar = Toplevel(root)
    top_buscar.iconphoto(True, PhotoImage(file="img/perro.png"))
    top_buscar.resizable(0, 0)
    top_buscar.title("BUSCAR REGISTRO")
    top_buscar.iconphoto(False, PhotoImage(file="img/huellas.png"))
    top_buscar.config(bg="gray80")

    # DAMOS UN TITULO AL FORMULARIO
    l_titulo = Label(
        top_buscar,
        fg="white",
        text="BUSQUEDA",
        font=("calibri bold", 15),
    )

    # CREAMOS LAS ETIQUETAS QUE INDICARAN QUE DATO INTRODUCIR EN CADA ENTRADA (ENTRY)
    l_busqueda = Label(
        top_buscar, text="BUSQUEDA:", font=("calibri bold", 11), bg="gray80"
    )

    # DEFINIMOS LAS VARIABLES QUE USAREMOS EN ESTE CASO 3
    id_busqueda_var, opcion = StringVar(), IntVar()

    # DEFINIMOS LOS CAMPOS DE ENTRADA "ENTRY"

    id_busqueda = Entry(top_buscar, width=100, textvariable=id_busqueda_var)

    # DEFINIMOS EL RADIOBUTTON PARA ELEGIR SOBRE QUE DATO HACER LA BUSQUEDA

    op_nombre = Radiobutton(
        top_buscar,
        text="NOMBRE",
        variable=opcion,
        value=1,
        bg="gray80",
    )
    op_raza = Radiobutton(
        top_buscar,
        text="RAZA",
        variable=opcion,
        value=2,
        bg="gray80",
    )
    op_id = Radiobutton(
        top_buscar,
        text="ID",
        variable=opcion,
        value=3,
        bg="gray80",
    )

    # UBICA LOS ELEMENTOS MEDIANTE EL SISTEMA DE GRILLA CON EL METODO GRID

    # TITULO
    l_titulo.grid(row=0, column=0, columnspan=2, sticky=W + E)
    l_titulo.config(bg="purple")  # Ponemos color de fondo al titulo

    # ETIQUETAS
    l_busqueda.grid(row=2, column=0, sticky=W, padx=10, pady=15)

    # RADIOBUTTON
    op_id.grid(row=1, column=1, sticky=W, padx=10, pady=1)
    op_raza.grid(row=1, column=1, sticky=W, padx=60, pady=1)
    op_nombre.grid(row=1, column=1, sticky=W, padx=110, pady=1)

    # CAMPOS DE ENTRADA

    id_busqueda.grid(row=2, column=1, padx=1, pady=15)

    
    b_bucar = Button(
        top_buscar, text="BUSCAR REGISTRO", font=("calibri bold", 11), command=search
    )
    b_bucar.grid(row=6, column=1, padx=1, pady=1, sticky=W + E)

    top_buscar.grab_set()
    top_buscar.focus_set()
    top_buscar.wait_window()

    top_buscar.mainloop()


# -------------------------------------------------FN LIMPIAR REGISTROS -------------------------------------------------------------


def limpiar():
    Lb1.delete(0, END)


# -------------------------------------------------FN TEMA --------------------------------------------------------------------------


def tema():
    result = askcolor(color="#00ff00", title="Seleccionar Color")

    try:
        root.configure(background=str(result[1]))
        listado.configure(background=str(result[1]))
        botonera.configure(background=str(result[1]))
    except:
        return


# --------------------------------------------------FN MODIFICAR------------------------------------------------------------------


def editar():
    def logica_editar():

        if (
            len(
                nombre_var.get()
                and raza_var.get()
                and vacunas_var.get()
                and tipo_var.get()
            )
            != 0
        ):

            validacion_id = re.compile(r"[0-9]")

            if re.match(validacion_id, str(id_edicion_var.get())):

                fecha = datetime.datetime.now().strftime("%y-%m-%d")

                hora = datetime.datetime.now().strftime("%H:%M:%S")

                datos = (
                    nombre_var.get(),
                    raza_var.get(),
                    vacunas_var.get(),
                    tipo_var.get(),
                    fecha,
                    hora,
                    id_edicion_var.get(),
                )

                bd = conn()

                c = bd.cursor()

                sql = """UPDATE registro SET  nombre = %s, raza = %s,  vacunas = %s, tipo = %s,   fecha = %s, hora = %s WHERE id = %s"""

                c.execute(sql, datos)

                bd.commit()

                if c.rowcount > 0:
                    messagebox.showinfo(
                        title="Mensaje",
                        message=str(c.rowcount) + " El registro fue modificado",
                    )
                else:
                    messagebox.showinfo(
                        title="Mensaje",
                        message="No se pudo modificar el registro o no existe",
                    )

                bd.close()

                id_edicion_var.set("")
                nombre_var.set("")
                raza_var.set("")
                vacunas_var.set("")
                tipo_var.set("")

            else:
                return messagebox.showwarning(
                    "ADVERTENCIA",
                    "EL CAMPO ID DE EDICION DEBE SER UN NUMERO",
                )
        else:
            return messagebox.showwarning(
                "ADVERTENCIA",
                "NO SE PERMITEN CAMPOS VACIOS\nSI DESEA BORRAR LOS DATOS ELIMINE EL REGISTRO\nSI DESEA DEJAR EN BLANCO UN CAMPO PRESIONE ESPACIO",
            )

    top_editar = Toplevel(root)
    top_editar.iconphoto(True, PhotoImage(file="img/perro.png"))
    top_editar.resizable(0, 0)
    top_editar.title("NUEVO REGISTRO")
    top_editar.iconphoto(False, PhotoImage(file="huellas.png"))
    top_editar.config(bg="gray80")

    # DAMOS UN TITULO AL FORMULARIO
    l_titulo = Label(
        top_editar,
        fg="white",
        text="EDICION DE REGISTROS",
        font=("calibri bold", 15),
    )

    # CREAMOS LAS ETIQUETAS QUE INDICARAN QUE DATO INTRODUCIR EN CADA ENTRADA (ENTRY)
    l_id_editar = Label(
        top_editar, text="ID A EDITAR:", font=("calibri bold", 11), bg="gray80"
    )
    l_nombre = Label(top_editar, text="NOMBRE:", font=("calibri bold", 11), bg="gray80")
    l_raza = Label(top_editar, text="RAZA:", font=("calibri bold", 11), bg="gray80")
    l_vacunas = Label(
        top_editar, text="VACUNAS:", font=("calibri bold", 11), bg="gray80"
    )
    l_tipo = Label(top_editar, text="TIPO:", font=("calibri bold", 11), bg="gray80")

    # DEFINIMOS LAS VARIABLES QUE USAREMOS EN ESTE CASO 3
    nombre_var, raza_var, vacunas_var, tipo_var, id_edicion_var = (
        StringVar(),
        StringVar(),
        StringVar(),
        StringVar(),
        StringVar(),
    )

    # DEFINIMOS LOS CAMPOS DE ENTRADA "ENTRY"
    id_editar = Entry(top_editar, width=100, textvariable=id_edicion_var)
    nombre = Entry(top_editar, width=100, textvariable=nombre_var)
    raza = Entry(top_editar, width=100, textvariable=raza_var)
    vacunas = Entry(top_editar, width=100, textvariable=vacunas_var)
    tipo = Entry(top_editar, width=100, textvariable=tipo_var)

    # UBICA LOS ELEMENTOS MEDIANTE EL SISTEMA DE GRILLA CON EL METODO GRID

    # TITULO
    l_titulo.grid(row=0, column=0, columnspan=2, sticky=W + E)
    l_titulo.config(bg="green")  # Ponemos color de fondo al titulo

    # ETIQUETAS
    l_id_editar.grid(row=1, column=0, sticky=W, padx=10, pady=1)
    l_nombre.grid(row=2, column=0, sticky=W, padx=10, pady=1)
    l_raza.grid(row=3, column=0, sticky=W, padx=10, pady=1)
    l_vacunas.grid(row=4, column=0, sticky=W, padx=10, pady=1)
    l_tipo.grid(row=5, column=0, sticky=W, padx=10, pady=1)

    # CAMPOS DE ENTRADA
    id_editar.grid(row=1, column=1, padx=1, pady=1)
    nombre.grid(row=2, column=1, padx=1, pady=1)
    raza.grid(row=3, column=1, padx=1, pady=1)
    vacunas.grid(row=4, column=1, padx=1, pady=1)
    tipo.grid(row=5, column=1, padx=1, pady=1)

    # CREAMOS EL BOTON DE EDITAR, DAMOS EL GRID

    b_editar = Button(
        top_editar,
        text="EDITAR REGISTRO",
        font=("calibri bold", 11),
        command=logica_editar,
    )
    b_editar.grid(row=6, column=1, padx=1, pady=1, sticky=W + E)

    id_editar.focus_set()

    top_editar.grab_set()
    top_editar.focus_set()
    top_editar.wait_window()

    top_editar.mainloop()


# --------------------------------------------------FRAME BOTONERA------------------------------------------------------------------

# CREAMOS EL CONTENEDOR DE LA BARRA DE BOTONES SUPERIOR DE LA APP

botonera = Frame(root, bg="papaya whip")
botonera.place(relx=0.01, rely=0.01, relheight=0.17, relwidth=0.98)

# DEFINIMOS LA IMAGEN A USAR EN EL BOTON NUEVO Y LO DEFINIMOS
# COMO NO VAMOS A USARLO MAS ADELANTE. NO DEFINIMOS UNA VARIABLE QUE APUNTE AL OBJETO
# EL CAMBIO DE TEMA ES SOLO PARA CAMBIAR EL COLOR DE FONDO DE LA APP.
# USAMOS PLACE PARA QUE LA APP SE ADAPTE A LA RESOLUCION QUE TENGA DISPONIBLE O PREFIERA EL USUARIO
img = Image.open("img/019-add.png")
img = ImageTk.PhotoImage(img)
Button(
    botonera,
    text="NUEVO",
    bg="gray90",
    font=("Arial bold", 10),
    image=img,
    compound="top",
    command=new_reg,
).place(relx=0, rely=0, relheight=1, relwidth=0.105)

# DEFINIMOS LA IMAGEN A USAR EN EL BOTON EDITAR Y LO DEFINIMOS
img2 = Image.open("img/018-edit.png")
img2 = ImageTk.PhotoImage(img2)
Button(
    botonera,
    text="EDITAR",
    bg="gray90",
    font=("Arial bold", 10),
    image=img2,
    compound="top",
    command=editar,
).place(relx=0.11, rely=0, relheight=1, relwidth=0.105)

# DEFINIMOS LA IMAGEN A USAR EN EL BOTON ELIMINAR Y LO DEFINIMOS
img3 = Image.open("img/015-remove.png")
img3 = ImageTk.PhotoImage(img3)
Button(
    botonera,
    text="ELIMINAR",
    bg="gray90",
    font=("Arial bold", 10),
    image=img3,
    compound="top",
    command=eliminar_registro,
).place(relx=0.22, rely=0, relheight=1, relwidth=0.105)

# DEFINIMOS LA IMAGEN A USAR EN EL BOTON ELIMINAR Y LO DEFINIMOS
img4 = Image.open("img/027-search.png")
img4 = ImageTk.PhotoImage(img4)
Button(
    botonera,
    text="BUSCAR",
    bg="gray90",
    font=("Arial bold", 10),
    image=img4,
    compound="top",
    command=buscar,
).place(relx=0.33, rely=0, relheight=1, relwidth=0.105)

# DEFINIMOS LA IMAGEN A USAR EN EL BOTON VER TODO Y LO DEFINIMOS
img5 = Image.open("img/005-infographic.png")
img5 = ImageTk.PhotoImage(img5)
Button(
    botonera,
    text="VER TODO",
    bg="gray90",
    font=("Arial bold", 10),
    image=img5,
    compound="top",
    command=ver_registros,
).place(relx=0.44, rely=0, relheight=1, relwidth=0.105)

# DEFINIMOS LA IMAGEN A USAR EN EL BOTON LIMPIAR Y LO DEFINIMOS
img6 = Image.open("img/023-remove.png")
img6 = ImageTk.PhotoImage(img6)
Button(
    botonera,
    text="LIMPIAR",
    bg="gray90",
    font=("Arial bold", 10),
    image=img6,
    compound="top",
    command=limpiar,
).place(relx=0.55, rely=0, relheight=1, relwidth=0.105)

# DEFINIMOS LA IMAGEN A USAR EN EL BOTON RESTAURAR Y LO DEFINIMOS
img7 = Image.open("img/024-reload.png")
img7 = ImageTk.PhotoImage(img7)
Button(
    botonera,
    text="RESTAURAR",
    bg="gray90",
    font=("Arial bold", 10),
    image=img7,
    compound="top",
    command=restaurar,
).place(relx=0.66, rely=0, relheight=1, relwidth=0.105)

# DEFINIMOS LA IMAGEN A USAR EN EL BOTON TEMA Y LO DEFINIMOS
img8 = Image.open("img/028-setting.png")
img8 = ImageTk.PhotoImage(img8)
Button(
    botonera,
    text="TEMA",
    bg="gray90",
    font=("Arial bold", 10),
    image=img8,
    compound="top",
    command=tema,
).place(relx=0.77, rely=0, relheight=1, relwidth=0.105)

# DEFINIMOS LA IMAGEN A USAR EN EL BOTON SALIR Y LO DEFINIMOS
img9 = Image.open("img/icon_cancelar.png")
img9 = ImageTk.PhotoImage(img9)
Button(
    botonera,
    text="SALIR",
    bg="gray90",
    font=("Arial bold", 10),
    image=img9,
    compound="top",
    command=root.destroy,
).place(relx=0.88, rely=0, relheight=1, relwidth=0.105)

# ---------------------------------------------------- FRAME PARA LISTBOX ----------------------------------------------------

# CREAMOS UN FRAME QUE CONTENGA EL LISTOBX

listado = Frame(root, bg="papaya whip")
listado.place(relx=0.01, rely=0.2, relheight=0.75, relwidth=0.99)

# DEFINIMOS EL LISTBOX Y SUS SCROLLBAR

scrollbar_y = Scrollbar(listado)
scrollbar_y.place(relx=0.975, rely=0.01, relheight=0.99, relwidth=0.02)

scrollbar_x = Scrollbar(listado)
scrollbar_x.place(relx=0, rely=0.95, relheight=0.05, relwidth=0.975)

Lb1 = Listbox(
    listado,
    bd=1,
    bg="gray90",
    font=("calibri bold", 14),
    yscrollcommand=scrollbar_y.set,
    xscrollcommand=scrollbar_x.set,
)

Lb1.place(relx=0, rely=0.01, relheight=0.95, relwidth=0.975)

scrollbar_y.config(orient=VERTICAL, command=Lb1.yview)
scrollbar_x.config(orient=HORIZONTAL, command=Lb1.xview)

# ----------------------------------------------------DEFINIMOS EL POPUP ----------------------------------------------------
def popup(event):
    bdatosMenu.post(event.x_root, event.y_root)


root.bind("<Button-3>", popup)  # DEFINIMOS EL EVENTO QUE ACTIVA EL POPUP

# ----------------------------------------------------DEFINIMOS EL MENU ----------------------------------------------------

barraMenu = Menu(root)
root.config(menu=barraMenu, width=300, height=300)

fileMenu = Menu(barraMenu, tearoff=0)
fileMenu.add_command(label="Salir", command=root.destroy)

bdatosMenu = Menu(barraMenu, tearoff=0)
bdatosMenu.add_command(label="Crear Nueva BD", command=crear_bd)
bdatosMenu.add_command(label="Crear Nueva Tabla", command=crear_tabla)
bdatosMenu.add_command(label="Crear Nuevo Registro", command=new_reg)
bdatosMenu.add_separator()
bdatosMenu.add_command(label="Ver Todos los Regitros", command=ver_registros)
bdatosMenu.add_separator()
bdatosMenu.add_command(label="Eliminar BD", command=eliminar_bd)
bdatosMenu.add_command(label="Eliminar Tabla", command=eliminar_tabla)
bdatosMenu.add_command(label="Eliminar Registro", command=eliminar_registro)

helpMenu = Menu(barraMenu, tearoff=0)
helpMenu.add_command(label="Acerca de...", command=ayuda)

barraMenu.add_cascade(label="Archivo", menu=fileMenu)
barraMenu.add_cascade(label="Base de Datos", menu=bdatosMenu)
barraMenu.add_cascade(label="Ayuda", menu=helpMenu)

# ---------------------------------------------------- FIN ----------------------------------------------------

root.mainloop()
