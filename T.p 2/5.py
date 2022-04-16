import random
def azar(inf,sup):
    rand=random.randin1t(inf,sup)
    return rand

def main():
    linf=int(input('Ingrese el limite inferior (natural): '))
    lsup=int(input('Ingrese el limite superior (natural): '))
    
    azar1=azar(linf,lsup)
    azar2=azar(azar1,lsup)
    azar3=azar(azar1,azar2)
    
    print('\n1- Limite inferior: {}, limite superior {}. Numero generado: {}'.format(linf,lsup,azar1))
    print('2- Limite inferior: {}, limite superior {}. Numero generado: {}'.format(azar1,lsup,azar2))
    print('3- Limite inferior: {}, limite superior {}. Numero generado: {}'.format(azar1,azar2,azar3))
main()