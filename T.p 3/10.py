def multa(va,vmax,e):
    vmin=vmax/2
    vmaxt=vmax+(vmax*15)/100
    vmint=vmin-(vmin*15)/100
    if e=='s':
        if va<vmint:
            rta='Recibe multa por entorpecer el tránsito'
        else:
            rta='No recibe multa'
    else:
        if va>vmint and va<vmax:
            rta='No recibe multa'
        elif vmax<va<vmaxt:
            rta='Advertecia'
        elif vmint<va<vmin:
            rta='Advertecia'
        elif va>vmaxt:
            rta='Recibe multa por exceso de velocidad'
        elif va<vmint:
            rta='Recibe multa por entorpecer el tránsito'
    return rta
def main():
    va=int(input('Velocidad del vehículo: '))
    vmax=int(input('Velocidad máxima: '))
    e=input('Emergencia (s/n):')
    
    m=multa(va,vmax,e)
    print('\n{}'.format(m))
main()