def primos(n):
    cont=0
    for i in range(1,n+1):
        if n%i==0:
            cont+=1
    if cont==2:
        return True
    else:
        return False
    
def main():
    n=int(input('Ingrese cantidad (numero natural): '))
    print('Primos entre 1 y {}\n'.format(n))
    cant=0
    for num in range(0,n+1):
        if primos(num)==True:
            print('{:<6}'.format(num), end='')
            cant+=1
            if cant%10==0:
                print('\n')
    print('\nPrimeros {} primos:\n'.format(n))
    i=0
    cont=0
    cant2=0
    while cont<n:
        if primos(i):
            cant2+=1
            cont+=1
            print('{:<6}'.format(i), end='')
            if cant2%10==0:
                print('\n')
        i+=1
main()