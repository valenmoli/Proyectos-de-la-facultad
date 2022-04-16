def func(p):
    if len(p)<2:
        print('La función ha retornado una palabra vacía')
    else:
        print('La funcion retorna:'+(p[-2]+p[-1])*3)

def main():
    pal=input('Ingrese palabra: ')
    func(pal)

main()