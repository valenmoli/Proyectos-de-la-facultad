def sueldototal(sb,h,c):
    st= sb+bono(sb)+plus(sb,h,c)
    return st
def bono(sb):
    if sb>2000:
        bn= (sb*15)/100
    elif sb<=2000:
        bn= (sb*20)/100
    return bn
def plush(sb,h):
    if h=='s':
        rta=(sb*5)/100
    else:
        rta=sb
    return rta
def plusc(sb,c):
    if c==1 or c==2 or c==3:
        rta=(sb*10)/100
    elif c==4 or c==5 or c==6:
        rta=(sb*12)/100
    elif c==7 or c==8 or c==9:
        rta=(sb*20)/100
    return rta
def plus(sb,h,c):
    plushijos=plush(sb,h)
    pluscat=plusc(sb,c)
    if c>=7:
        plustotal= pluscat
    else:
        plustotal= plushijos+pluscat
    return plustotal
def main():
    sueldob=int(input('Imgrese el sueldo base: '))
    hijos=input('Tiene hijos? (s/n): ')
    categoria=int(input('Ingrese categoría (1-9): '))
    if (hijos!='s' and hijos!='n') or categoria>9 or categoria<1:
        print('\nError en los datos')
    else:
        sueldot=sueldototal(sueldob,hijos,categoria)    
        print('El sueldo total será de ${:.2f}'.format(sueldot))
main()