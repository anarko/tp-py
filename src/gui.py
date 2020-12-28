import tkinter 

def vaciar_from_frame():
    # elimino el interior del frame para crearlo de nuevo 
    for cosa in formFrame.winfo_children():
           cosa.destroy()



def nuevo_registro():
    # ventana nueva
    #filewin = tkinter.Toplevel(main)
    #button = tkinter.Button(filewin, text="Do nothing button")
    #button.pack()    
    
    vaciar_from_frame()

    label = tkinter.Label(formFrame, text = "Nuevo registro")
    label.pack()

    my_entry = tkinter.Entry(formFrame, width = 20)
    my_entry.insert(0,'Campo1')
    my_entry.pack(padx = 5, pady = 5)
 
    my_entry2 = tkinter.Entry(formFrame, width = 15)
    my_entry2.insert(0,'campo2')
    my_entry2.pack(padx = 5, pady = 5)
    
    button1 = tkinter.Button(formFrame, text = "Guardar", command=guardar_registro )
    button1.pack(padx = 3, pady = 3)
    


main = tkinter.Tk()
main.geometry("200x150")
mainWindow = tkinter.Frame(main)
mainWindow.pack()
 
mainmenu = tkinter.Menu(mainWindow)
mainmenu.add_command(label = "Nuevo", command= nuevo_registro)  
mainmenu.add_command(label = "Ver", command= nuevo_registro)
mainmenu.add_command(label = "Exit", command= main.destroy)
 
formFrame = tkinter.Frame(main)
formFrame.pack(side=tkinter.RIGHT)

main.title("Crud y ques")
main.config(menu = mainmenu)
main.mainloop()