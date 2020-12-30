
def fecha():
    f = input("Fecha:")
    ff = f.split("/")
    todo_ok = True
    if (len(ff) != 3) :
        print("Formato incorrecto debe ser DD/MM/AAAA")        
        todo_ok = False
    if len(ff[0]) != 2 or int(ff[0]) not in [x for x in range(1,32)]:
        print("Formato del dia incorrecto o fecha invalida : ",ff[0])
        todo_ok = False
    if len(ff[1]) != 2 or int(ff[1]) not in [x for x in range(1,13)]:
        print("Formato del mes incorrecto o fecha invalida",ff[1])
        todo_ok = False
    if len(ff[2]) != 4:
        print("Formato del año incorrecto o fecha invalida",ff[2])
        todo_ok = False
    
    if  todo_ok:
        print(ff[2]+"/"+ff[1]+"/"+ff[0])
    
fecha()