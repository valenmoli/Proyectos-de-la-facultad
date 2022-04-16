def booleana(n1,n2,n3):
    if n1>n2 and n2>n3:
        if (n1-n2)==(n2-n3):
            rta=1
        else:
            rta=0
    elif n1>n2 and n2<n3 and n1>n3:
            if (n1-n3)==(n3-n2):
                rta=1
            else:
                rta=0
    elif n1<n2 and n1<n3 and n3<n2:
        if (n2-n3)==(n3-n1):
            rta=1
        else:
            rta=0
    elif n1<n2 and n1>n3 and n1<n2:
        if (n2-n1)==(n1-n3):
            rta=1
        else:
            rta=0            
    elif n1<n3 and n2<n3 and n1>n2:
        if (n3-n1)==(n1-n2):
            rta=1
        else:
            rta=0
    elif n1<n3 and n2<n3 and n1<n2:
        if (n3-n2)==(n2-n1):
            rta=1
        else:
            rta=0
    else:
        rta=0
    return rta
def main():
    n1=int(input('Ingrese el primer número: '))
    n2=int(input('Ingrese el segundo número: '))
    n3=int(input('Ingrese el tercer número: '))
    
    inv=booleana(n1,n2,n3)
    rta= inv*'' + (1-inv)*'No'
    print('{} Estan igualmente distanciados!'.format(rta))
    
main()
    
        
    
            