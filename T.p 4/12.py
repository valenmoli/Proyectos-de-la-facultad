def invocar(b):
    for i in range(b+1):
        print('*'*i)
        i+=1
    
def main():
    base=int(input('Ingrese base: '))
    while base<3:
        print('Erorr, debe ser mayor o igual a 3.')
        base=int(input('Ingrese base: '))
    invocar(base)
main()