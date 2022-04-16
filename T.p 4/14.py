def invocar (h):
    i=1
    while i<=h:
        print('*'*i)
        i+=2
    i-=2        
    while i!=1:
        i-=2
        print('*'*i)
           
def main():
    h=int(input('Ingrese base: '))
    while h<5 or h%2==0:
        print('Erorr, debe ser mayor o igual a 3 e impar.')
        h=int(input('Ingrese base: '))
    invocar(h)
main()