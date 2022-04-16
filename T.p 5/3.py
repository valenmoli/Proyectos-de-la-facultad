def palabraverif(p):
    for i in p:
        if (i>'A' and i<'Z') or (i>'a' and i<'z'):
            return False
        else:
            return True
def primeraMitad(p):
    
    rta=p[0:len(p)//2]
    
    return rta
    
def main():
    pal=input('Ingrese una palabra de longitud par: ')
    while len(pal)%2!=0 or lpalabraverif(pal):
        pal=input('Error. Ingrese una palabra de longitud par: ')
    
    invocar=primeraMitad(pal)
    print('La funcion a retornado: {}'.format(invocar))
    
main()