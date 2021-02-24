#Library import
import pathlib
from tkinter import Tk, PhotoImage
#Local import
import gui

APP_PATH = str(pathlib.Path().absolute())

class BuclePpal:
			
	def start_me_up(self):
		""" Inicia el bucle principal de la aplicacion
		"""
		root = Tk()
		root.config(bg="papaya whip") 
		root.state("normal")
		root.minsize(800, 600)
		root.iconphoto(False, PhotoImage(file=APP_PATH+"/img/huellas.png"))
		root.title("MASCOTAS SOFT 4.0a1")    
		gui.CrudTk(root)
		root.mainloop()
		
if __name__ == "__main__":
    app = BuclePpal()
    app.start_me_up()
