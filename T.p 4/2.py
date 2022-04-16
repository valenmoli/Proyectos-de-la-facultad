def main():
    print('Ingrese numeros enteros positivos (finalece con 0): ')
    n=int(input())
    my=n ; mn=n
    while n!=0:
        if n>my:
            my=n
        if n<mn:
            mn=n
        n=int(input())
            
    print('El mayor es {} y el menor es {}.'.format(my,mn))
main()