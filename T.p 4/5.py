def todoslosn():
    for n in range(1000,9999+1):
        unidades=n%10
        decenas=n%100//10
        centenas=n%1000//100
        unidadesm=n//1000
        if unidades+centenas==decenas+unidadesm:
            print(n,end=' ')
        else:
            ''
    
def booleana(n):
    unidades=n%10
    decenas=n%100//10
    centenas=n%1000//100
    unidadesm=n//1000
    if unidades+centenas==decenas+unidadesm:
        return True
    else:
        return False
def main():
    n=int(input('Ingrese numero de 4 cifras: '))
    while len(str(n))!=4:
        n=int(input('Ingrese numero de 4 cifras: '))
    print(booleana(n))
    
    invocar=todoslosn()
main()