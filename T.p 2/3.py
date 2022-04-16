def paridad(n):
    b0=n%10
    b1=n//10%10
    b2=n//100%10
    b3=n//1000%10
    b4=n//10000%10
    b5=n//100000%10
    b6=n//1000000%10
    b7=n//10000000%10
    suma=b0+b1+b2+b3+b4+b5+b6+b7
    
    return suma%2
def main():
    num=int(input('Ingrese un numero binario de hasta 8 bits:'))
    
    result=paridad(num)
    
    print('Bit de paridad generado {}'.format(result))
    
main()