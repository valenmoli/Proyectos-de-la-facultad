def cierre(e,p):
    if len(e)==2 and len(p)>0:
        x=e[0]+p+e[1]
    else:
        x=''
        
    return x

def main():
    ext=input('Ingrese extremos: ')
    pal=input('Ingrese palabra: ')
    
    if cierre(ext,pal):
        print('La función retornó: {}'.format(cierre(ext,pal)))
    else:
        print('La función ha retornado una palabra vacía')
main()