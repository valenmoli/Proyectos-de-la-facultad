def booleana(n1,n2):
    if n1<n2:
        rta='NO'
    elif n1>=n2:
        rta='SI'
    return rta    
def main():
    
    num1=int(input('Ingrese un número A: '))
    num2=int(input('Ingrese un número B: '))
    
    print('\n{} cumple condicion.'.format(booleana(num1,num2)))
    
main()
    
    
    