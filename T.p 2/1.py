def area(l1,l2,l3):
    p=(l1+l2+l3)/2
    
    at=(p*(p-l1)*(p-l2)*(p-l3))**(1/2)
    
    return at
def main():
    l1=int(input('Ingrese lado 1:'))
    l2=int(input('Ingrese lado 2:'))
    l3=int(input('Ingrese lado 3:'))
    
    result=area(l1,l2,l3)
    
    print('\nEl area del triangulo es = {:.2f}'.format(result))
    
main()
    