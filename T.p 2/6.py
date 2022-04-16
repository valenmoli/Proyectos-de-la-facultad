import random

def booleana(v1,v2):
    azar=random.randint(0,1)
    r1=v1*azar
    r2=v2*(1-azar)
    rta= r1+r2
    
    return rta

def main():
    av1=input('Ingrese alternativa 1 para vestimenta: ')
    av2=input('Ingrese alternativa 2 para vestimenta: ')
    ap1=input('Ingrese alternativa 1 para plato: ')
    ap2=input('Ingrese alternativa 2 para plato: ')
    ab1=input('Ingrese alternativa 1 para bebida: ')
    ab2=input('Ingrese alternativa 2 para bebida: ')
    
    vestimenta= booleana(av1,av2)
    plato= booleana(ap1,ap2)
    bebida= booleana(ab1,ab2)
    
    print('\nCena al azar: {}, {} y {}'.format(vestimenta,plato,bebida))
    
    
main()