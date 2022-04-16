def operacion(n1,n2,op):
    if op=='+':
        r=n1+n2
    elif op=='-':
        r=n1-n2
    elif op=='*':
        r=n1*n2
    elif op=='/':
        r=n1/n2
    return r
def main():
    
    num1= int(input('Ingrese el primer número: '))
    num2= int(input('Ingrese el segundo número: '))
    op=input('Ingrese la operación (+,-,*,/): ')
    if op=='+' or op=='-' or op=='*' or op=='/':
        print('\n{} {} {} = {}'.format(num1,op,num2,operacion(num1,num2,op)))
        
    else:
        print ('\nError en la operacion')
       
main()