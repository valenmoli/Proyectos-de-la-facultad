#EJERCICIO 8
def cargardic2(dic,nom):
    a=open(nom,"r")
    lineas=a.readlines()
    a.close()
    for linea in lineas:
        linea=linea[:-1]
        datos=linea.split(",")
        dic[int(datos[0])]=[datos[1],int(datos[2]),int(datos[3]),int(datos[4])]
    
    
def cargardic13(dic,nom):     #sirve para provincias y paises (.csv)
    a=open(nom,"r")
    lineas=a.readlines()
    a.close()
    for linea in lineas:
        linea=linea[:-1]
        datos=linea.split(",")
        dic[int(datos[0])]=[datos[1],int(datos[2])]

def poblacion(id_prov):
    dic_prov={}
    dic_loc={}
    cargardic13(dic_prov,"provincias.txt")
    cargardic2(dic_loc,"localidades.txt")
    
    suma=0
    for clave in dic_loc:
        if dic_loc[clave][1]==id_prov:
            suma+=dic_loc[clave][3]
            
    provincia= dic_prov[id_prov][0]
    
    print(provincia+": {} Habitantes".format(suma))
            
def localidadMaxima():
    dic_prov={}
    dic_loc={}
    dic_pais={}
    cargardic13(dic_prov,"provincias.txt")
    cargardic13(dic_pais,"paises.txt")
    cargardic2(dic_loc,"localidades.txt")
    
    pmax=0
    for clave in dic_loc:
        if dic_loc[clave][3]>pmax:
            pmax=dic_loc[clave][3]
            
    id_loc=""
    id_prov=""
            
    for clave in dic_loc:
        if dic_loc[clave][3]==pmax:
            id_loc=clave
            id_prov=dic_loc[clave][1]
    
    localidad=dic_loc[id_loc][0]
    provincia=dic_prov[id_prov][0]
    pais=dic_pais[(dic_prov[id_prov][1])][0]
    
    print("Población: {}".format(pmax))
    print("Localidad: {}".format(localidad))
    print("Provincia: {}".format(provincia))
    print("Pais: {}".format(pais))

    
def main():
    id_prov=int(input("Ingrese el ID_provincia: "))
    while id_prov<0:
        id_prov=int(input("Error, ingrese el ID_provincia: "))
    poblacion(id_prov)
    localidadMaxima()
        
    
main()