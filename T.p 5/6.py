def esletra(l):
    for i in l:
        if (i>'a' and i<'z') or (i>'A' and i<'Z'):
            return True
        else:
            return False
        
def booleana(f):
    frasereves=''
    i=1
    while i<len(f):
         frasereves+=f[len(f)-i]
         long=-1
         i+=1
    if f==frasereves:
        return True
    else:
        return False
    
def main():
    frase=input('ingrese fase: ')
    
    if booleana(frase):
        print('La frase es palíndroma!')
    else:
        print('La no frase es palíndroma!')
main()