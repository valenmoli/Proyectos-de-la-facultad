def main():
    pares=0
    while pares<5:
        n=int(input('Ingrese numero entero: '))
        if n%2==0:
            pares+=1
            if n%4==0:
                m4='Tambien es multiplo de 4.'
                print('Numero Par. {} Total de numeros pares ingresador: {}'.format(m4,pares))
            else:
                print('Numero Par. Total de numeros pares ingresados {}'.format(pares))
        else:
            ''
    print('\nFIN')
main()
            