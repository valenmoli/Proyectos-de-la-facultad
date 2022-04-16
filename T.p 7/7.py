def cargarDic():
    dic= {}
    file=open('ejercicio7.csv','r')
    for line in file:
        linea=line.split(',')
        dic[int(linea[2])]=[linea[0],linea[1]]
    file.close
    return dic
def mostrarArchivo():
    linea=''
    file=open('ejercicio7.csv','r')
    for line in file:
        print(line,end='')
    file.close

def agregarRegistro():
    dic= cargarDic()
    dni=int(input('ingrese dni: '))
    while dni in dic:
        dni=int(input('error. ingrese nuevamente: '))
    while dni<1:    
        dni=int(input('error. ingrese nuevamente: '))
    nombre=input('ingrese nombre: ')
    apellido=input('ingrese apellido: ')
    dic[dni]=[nombre,apellido]
    string=nombre+','+apellido+','+str(dni)+'\n'
    file=open('ejercicio7.csv','a')
    file.write(string)
    file.close
    
def elimRegistro():
    dic=cargarDic()
    dni=int(input('ingrese dni del cual quiere eliminar '))
    while dni<1 or dni not in dic:
        dni=int(input('error. ingrese nuevamente: '))
    if dni in dic:
        del dic[dni]
    total=''
    file=open('ejercicio7.csv','w')
    for key in dic:
        total+=dic[key][0]+','+dic[key][1]+','+str(key)+'\n'
        file.write(total)
        file.close
        
def buscarRegistro():
    dic=cargarDic()
    op=int(input('si buscas por dni marque 1, si busca por apellido marque 2: '))
    while op<1 or op>2:
         op=int(input('ERROR. si buscas por dni marque 1, si busca por apellido marque 2: '))
    if op==1:
        dni=int(input('ingrese dni a buscar: '))
        while dni not in dic:
            dni=int(input('ERROR. ingrese dni a buscar: '))
            
        print(dic[dni][0]+','+dic[dni][1]+','+str(dni))
            
    if op==2:
        ape=input('ingrese apellido a buscar: ')
        for key in dic:
            if dic[key][1]==ape:
                print(dic[key][0]+','+ape+','+str(key))
                
def ordenarArchivo():
    dic=cargarDic()
    op=int(input('si buscas ordenar por dni marque 1, si busca  ordenar por apellido marque 2, si busca ordenar por nombre marque 3:  '))
    while op<1 or op>3:
        op+=int(input('ERROR. si buscas ordenar por dni marque 1, si busca  ordenar por apellido marque 2, si busca ordenar por nombre marque 3:  '))
    if op==1:
        lst=list(dic.keys())
        for i in range(len(lst)-1):
            for j in range(i+1,len(lst)):
                if lst[i]>lst[j]:
                    lst[i],lst[j]=lst[j],lst[i]
        arch=open("ejercicio7.csv","w")
        total=""
        for clave in lst:
            total+=dic[clave][0] + "," + dic[clave][1] + "," + str(clave) + "\n"
        
        arch.write(total)
        arch.close()            
            
    if op==2:
        lst=list(dic.keys())
        for i in range (0,len(lst)-1):
            for j in range(i+1,len(lst)):
                if dic[lst[i]][1]>dic[lst[j]][1]:
                    lst[i],lst[j]=lst[j],lst[i]
        total=''
        file=open('ejercicio7.csv','w')
        for key in lst:
            total+=dic[key][0] + "," + dic[key][1] + "," + str(key) + "\n"
        file.write(total)
        file.close()
            
        
    if op==3:
        lst=dic.keys()
        for i in range (0,len(lst)-1):
            for j in range(i+1,len(lst)):
                if dic[lst[i][0]]> dic[lst[j]][0]:
                    lst[i][0],lst[j][0]=lst[j][0],lst[i][0]    
    
    
    
    
    
def main():
    print('1. AGREGAR REGISTRO\n2. ELIMINAR REGISTRO\n3. BUSCAR REGISTRO\n4. ORDENAR ARCHIVO POR\n5. MOSTRAR ARCHIVO\n6. SALIR')
    op=int(input('Ingrese valor: '))
    while op<1 or op>6:
        op=int(input('ERROR Ingrese nuevamente: '))
    while op!=6:
        if op==1:
            agregarRegistro()
        if op==2:
            elimRegistro()
        if op==3:
            buscarRegistro()
        if op==4:
            ordenarArchivo()
        if op==5:
            mostrarArchivo()
        op=int(input('Ingrese valor: '))
    print('Fin')
        
            
main()