def tiponum(n):
    if n%1==0 and n>0:
        num='entero natural'
    elif n%1==0 and n<0:
        num='entero'
    elif n%1 !=0:
        num='real'
    elif n==0:
        num='entero'
    return num
def tiposigno(n):
    if n>0:
        signo='positivo'
    elif n<0:
        signo='negativo'
    elif n==0:
        signo='cero'
        
    return signo

def main():
    n=float(input('Ingrese un núnmero: '))
    print('EL numero es {} y {}'.format(tiposigno(n),tiponum(n)))
    
main()