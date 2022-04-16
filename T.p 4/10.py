def invocar(b,h):
    i=0
    for i in range (h):
        print('*'*b)
       
def main():
    base=int(input('Ingrese base: '))
    while base<2:
        print('Erorr, debe ser mayor o igual a 2.')
        base=int(input('Ingrese base: '))
    h=int(input('Ingrese altura: '))
    while h<2:
        print('Erorr, debe ser mayor o igual a 2.')
        h=int(input('Ingrese altura: '))
    
    invocar(base,h)
main()