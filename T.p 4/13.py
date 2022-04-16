def invocar(b):
    i=1
    while i<=b:
        esp=(b-i)//2
        print(' '*esp+'*'*i+' '*esp)
        i+=2
def main():
    base=int(input('Ingrese base: '))
    while base<3 or base%2==0:
        print('Erorr, debe ser mayor o igual a 3 e impar.')
        base=int(input('Ingrese base: '))
    invocar(base)
main()