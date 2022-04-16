def invocar(d):
    i=1
    while i<=d:
        esp=(d-i)//2
        print(' '*esp+'*'*i+' '*esp)
        i+=2
    i-=2
    while i!=1:
        i-=2
        esp=(d-i)//2
        print(' '*esp+'*'*i+' '*esp)
        

def main():
    d=int(input('Ingrese base: '))
    while d<5 or d%2==0:
        print('Erorr, debe ser mayor o igual a 3 e impar.')
        d=int(input('Ingrese base: '))
    invocar(d)
main()