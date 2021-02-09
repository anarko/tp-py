from tkinter import Tk
from tkinter import mainloop
from tkinter import PhotoImage
from vista import gui


class manage(Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.config(bg="papaya whip")
        self.state("normal")
        self.minsize(1080, 768)
        self.iconphoto(False, PhotoImage(file="src/huellas.png"))
        self.title("MASCOTAS SOFT 4.0")
        self.a = gui(self, x=0.01, y=0.01, h=0.17, w=0.98)
    
    

if __name__ == "__main__":
    a = manage()
    a.mainloop()
