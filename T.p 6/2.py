
def estaenlista(n,l):
    return n in l

def cargarLista():
    num=int(input('Ingrese numero entero positivo. Ingrese 0 para terminar: '))
    lista=[]
    while num !=0:
        while num > 0 and not estaenlista(num,lista):
            lista.append(num)
            num=int(input())
        
    print('La lista contiene:\n{}'.format(lista))
            
        
cargarLista()