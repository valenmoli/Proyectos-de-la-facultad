def informe(arch):
    file=open(arch,'r')
    i=1
    cont=0
    suma=0
    for linea in file:
        cont+=1
        if i==1:
            i=0
            mayor=int(linea)
            menor=int(linea)
        if int(linea)>mayor:
            mayor=int(linea)
        if int(linea)<menor:
            menor=int(linea)
        suma+=int(linea)
    lista=['Valor maximo {}'.format(mayor),'Valor minimo {}'.format(menor),'Valor promedio {}'.format(suma/cont),"Cantidad {}".format(cont)]
    file.close()        
    return lista
    
def main():
    arch=informe('1.1.txt')
    print(arch)
    
main()