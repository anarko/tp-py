# ----------------------------------------------------IMPORTAMOS LO QUE USAREMOS ---------------------------------------------------------
from tkinter import Tk, PhotoImage
import gui

# TODO: el form para editar


if __name__ == "__main__":
    root = Tk()
    root.config(bg="papaya whip")

    root.state("normal")
    root.minsize(800, 600)
    root.iconphoto(False, PhotoImage(file="img/huellas.png"))
    root.title("MASCOTAS SOFT 4.0a1")    
    gui.CrudTk(root)
    root.mainloop()
