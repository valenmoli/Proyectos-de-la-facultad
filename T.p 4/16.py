def invocar(a):
    i=1
    alt=a
    while i<=alt:
        if i==1 or i==alt:
            print('*'*a)
            i+=1
            alt-=1
        else:
            print('*'+' '*(i-1)+'*'*(a-2*i)+' '*(i-1)+'*')
            i+=1
            alt-=1
        
def main():
    ancho=int(input('Ingrese ancho: '))
    while ancho<7 or ancho%2==0:
        print('Erorr, debe ser mayor o igual a 3 e impar.')
        ancho=int(input('Ingrese ancho: '))
    invocar(ancho)
main()