def invocar(b,h):
    i=1
    while i<=h:
        if i==1 or i==h:
            print('*'*b)
            i+=1
        else:
            print('*'+' '*(b-2)+'*')
            i+=1
       
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