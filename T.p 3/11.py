def mensaje(c1,c5,m):
    if c1>=m or c5*5==m or (m%10<=c1 and m//10<=c5*5):
        fra= 'Es posible cubrir el tendido'
    else:
        fra= 'No es posible cubrir el tendido'
    return fra
        
def main():
    _1= int(input('Cantidad de canos de 1 metro: '))
    _5= int(input('Cantidad de canos de 5 metros: '))
    m= int(input('Metros totales por cubrir: '))
    invocar= mensaje(_1,_5,m)
    print('\n{}'.format(invocar))
main()