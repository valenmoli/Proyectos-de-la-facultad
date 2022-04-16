def booleana(n):
    if n%2==0:
        n2=int(input('Ingrese un numero menor a {}: '.format(n)))
        if n2<n:
            rta='Correcto'
        else:
            rta='Incorrecto'
    elif n%2!=0:
        n2=int(input('Ingrese un número mayor que {}: '.format(n)))
        if n2>n:
            rta='Correcto'
        else:
            rta='Incorrecto'
    return rta
def main():
    num=int(input('Ingrese un número entero positivo: '))
    rta=booleana(num)
    print('{}!'.format(rta))
    
main()