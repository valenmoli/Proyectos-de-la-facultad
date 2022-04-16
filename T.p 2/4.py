import math
def areaCirc(diametro):    
    ac1=(math.pi*(diametro)**2)/4    
    
    return ac1

def areaCuad(lado):
    aC= lado*lado
    
    return aC
def areaNegra(lado):
    ac1=areaCirc(lado*(2/3))
    ac2=areaCirc(lado*(1/3))
    aC=areaCuad(lado)
    aN= aC-ac1-2*ac2
    
    return aN
def main():
    lado=int(input('Ingrese lado:'))
    
    aN=areaNegra(lado)
    aC=areaCuad(lado)
    aN_100= (aN*100)/(lado**2)
    
    print('El area negra es {:.2f} y es un {:.2f}% del area total del cuadrado'.format(aN,aN_100))
    
main()