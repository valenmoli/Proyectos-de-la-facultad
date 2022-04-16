def cargarLstAlu():
    l=[]
    dni=int(input('ingrese dni: '))
    l.append(dni)
    nomb=input('ingrese nombre: ')
    l.append(nomb)
    edad=int(input('ingrese edad'))
    l.append(edad)
    return l
    
def ordenarAluxDNI(lnazi):
    for i in range (0,len(lnazi)-1):
        for j in range (i+1,len(lnazi)):
            a=lnazi[i]
            b=lnazi[j]
            if a[0] >b[0]:
                aux=a[0] 
                a[0]=b[0]
                b[0]=aux
            
def main():
    x=int(input('1. Cargar lista\n2. Ordenar lista\n3. Salir'))
    while x!=3:
        if x==1:
            lnazi=cargarLstAlu()
            print(lnazi)
            x=int(input('1. Cargar lista\n2. Ordenar lista\n3. Salir'))
        if x==2:
            orden=(ordenarAluxDNI(lnazi))
            print(orden)
            x=int(input('1. Cargar lista\n2. Ordenar lista\n3. Salir'))
    
    print('Fin')
    
main()