
def print_num():
    n = int(input("Número:"))
    l1=l2=""
    for h in range(n+1):
        l1 = l1+str(h)+","
        l2 = l2+str(n-h)+","
    
    print(l1[:-1])
    print(l2[:-1])
    