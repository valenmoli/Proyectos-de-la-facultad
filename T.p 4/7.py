def main():
    n=int(input('Ingresar nota: '))
    cont_apl=0
    cont_apr=0
    cont_prom=0
    total=0
    while n!=0:
        if n>0 and n<4:
            cont_apl+=1
            total+=n
        elif n>=4 and n<=7:
            cont_apr+=1
            total+=n
        elif n>7 and n<=10:
            cont_prom+=1
            total+=n
        n=int(input('Ingresar nota: '))
    cont=cont_apl+cont_apr+cont_prom
    promedio=total/cont
    print('Cantidad de aplazos {} (%{:.2f})'.format(cont_apl,(cont_apl/cont)*100))
    print('Cantidad de aprobados {} (%{:.2f})'.format(cont_apr,(cont_apr/cont)*100))
    print('Cantidad de promocionados {} (%{:.2f})'.format(cont_prom,(cont_prom/cont)*100))
    print('Promedio total {:.2f}'.format(promedio))

main()