def booleana(d,m,a):
    if (m==1 or m==3 or m==5 or m==6 or m==7 or m==8 or m==10 or m==12):
        if (d<=31 and d>0):
            rta='correcta'
        else:
            rta='incorecta'
    elif (m==4 or m==6 or m==9 or m==11):
        if (d<=30 and d>0):
            rta='correcta'
        else:
            rta='incorecta'
    elif m==2:
        if a%4==0:
            if (d<=29 and d>0):
                rta='correcta'
            else:
                rta='incorecta'
        elif a%4!=0:
            if (d<=28 and d>0):
                rta='correcta'
            else:
                rta='incorecta'    
    return rta
def main():
    dia=int(input('Ingrese el día: '))
    mes=int(input('Ingrese el mes: '))
    año=int(input('Ingrese el año: '))
    
    print('\nLa fecha es {}.'.format(booleana(dia,mes,año)))
        
main()
    