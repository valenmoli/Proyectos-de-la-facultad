def ordenar(n1,n2,n3):
    if n1>n2 and n1>n3 and n2>n3:
        print('Los numeros ordenados en forma ascendente son:\n{}\n{}\n{}'.format(n3,n2,n1))
    elif n1>n2 and n1>n3 and n2<n3:
        print('Los numeros ordenados en forma ascendente son:\n{}\n{}\n{}'.format(n2,n3,n1))
    elif n1<n2 and n1>n3 and n2>n3:
        print('Los numeros ordenados en forma ascendente son:\n{}\n{}\n{}'.format(n3,n1,n2))
    elif n1<n2 and n1<n3 and n2>n3:
        print('Los numeros ordenados en forma ascendente son:\n{}\n{}\n{}'.format(n1,n3,n2))
    elif n1<n2 and n1<n3 and n2<n3:
        print('Los numeros ordenados en forma ascendente son:\n{}\n{}\n{}'.format(n1,n2,n3))
    elif n1>n2 and n1<n3 and n2<n3:
        print('Los numeros ordenados en forma ascendente son:\n{}\n{}\n{}'.format(n2,n1,n3))
        
def main():
    num1=int(input('Ingrese el primer número: '))
    num2=int(input('Ingrese el segundo número: '))
    num3=int(input('Ingrese el tercero número: '))
    ordenar(num1,num2,num3)
main()