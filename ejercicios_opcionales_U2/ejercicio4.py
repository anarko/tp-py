

def vocales():
    p = input("Palabra:")
    v = {'a':0,'e':0,'i':0,'o':0,'u':0}
    for l in p:
        if l in v:
            v[l] = v[l]+1
    print(v)
            
        