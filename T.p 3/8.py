def promedio(p1,p2,p3,p4):
    prom=(p1+p2+p3+p4)/4
    return prom
def main():
    p1=int(input('Ingrese la nota del primer parcial: '))
    p2=int(input('Ingrese la nota del segundo parcial: '))
    p3=int(input('Ingrese la nota del tercer parcial: '))
    prom=(p1+p2+p3)/3
    if prom>=7:
        result='promociona la materia'
    elif prom>=4:
        result='deberá rendir final'
    elif prom<4:
        p4=int(input('Ingrese la nota del recuperatorio: '))
        prom2=promedio(p1,p2,p3,p4)
        if p4>=4:
            result='deberá rendir final'
        else:
            result='fue aplazado'
    
    if prom>=4:
        print('\nPromedio general= {:.1f} \nEl alumno {}'.format(prom,result))
        
    else:
        print('\nPromedio general= {:.1f} \nEl alumno {}'.format(prom2,result))
        
main()