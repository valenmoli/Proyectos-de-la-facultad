def cargarLista():
    num=int(input('Ingrese un numero. Ingrese 0 para terminar: '))
    lista=[]
    while num !=0:
        if num not in lista:
            lista.append(num)
            num=int(input())
        else:
            num=int(input())
    
    return lista
def cargarConjuntos(lista1,lista2):
    print('Cargando lista 1...')
    lista1=cargarLista()
    print('Cargando lista 2...')
    lista2=cargarLista()
    
    return lista1, lista2

def union(lista1,lista2):
    lunion=[]
    for i in lista1:
        lunion.append(i)
    for x in lista2:
        if x not in lunion:
            lunion.append(x)
    return lunion

def interseccion(lista1,lista2):
    linter=[]
    for i in lista1:
        if i in lista2:
            linter.append(i)
        
    return linter

def diferencia(lista1,lista2):
    ldif=lista1
    for i in lista2:
        if i in ldif:
            ldif.remove(i)
        else:
            ldif.append(i)
    return ldif
def diferenciaSimetrica(lista1,lista2):
    ldifs=[]
    for i in lista1:
        ldifs.append(i)
    for i in lista2:
        ldifs.append(i)
    union=union(lista1,lista2)
    for i in ldifs:
        if i in union:
            remove

def main():
    x=0
    lista1=[]
    lista2=[]
    while x==0 or x!=6:
        x=int(input('1. CARGAR CONJUNTOS \n2. UNION\n3. INTERSECCION\n4. DIFERENCIA (A-B)\n5. DIFERENCIA SIMÉTRICA\n6. SALIR\nIngrese el valor de la opción: '))
        while x !=6 and not x<1 and not x>6:
            if x==1:
                
                lista1,lista2=cargarConjuntos(lista1,lista2)
                x=0
            if x==2:
                print(union(lista1,lista2))
                x=0
            if x==3:
                print(interseccion(lista1,lista2))
                x=0
            if x==4:
                print(diferencia(lista1,lista2))
                x=0
            if x==5:
                print(diferenciaSimetrica(lista1,lista2))
                x=0
    print('Fin.')
    
    
main()