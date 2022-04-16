import math
def raiz(rad,ind):
    num=math.pow(rad,1/ind)
    
    return num
def main():
    x=int(input('Ingrese el radicando (numero real):'))
    n=int(input('Ingrese el índice (numero natural):'))
    
    result= raiz(x,n)
    
    print('\nLa raiz {} de {} es = {:f}'.format(n,x,result))
main()