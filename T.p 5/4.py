def esletra(t):
    for i in t:
        if (i>'a' and i<'z') or (i>'A' and i<'Z'):
            return True
        else:
            return False
def principioFin(t):
    i=0
    p=''
    while i<len(t):
        while i<len(t) and not esletra(t[i]):
            i+=1
        
        while i<len(t) and esletra(t[i]):
            p=
            
            
        
    
    
def main():
    texto=input('Ingrese un texto: ')
    
    if principioFin(texto):
        print('bien')
    else:
        print('mal')
    
    
    
main()