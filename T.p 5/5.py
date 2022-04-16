def rotacion(t):
    
    nuevo_str=t[(len(t)//2):len(t)]+t[0:(len(t)//2)]
    
    return nuevo_str
    
    
def main():
    text= input('Ingrese texto: ')
    while len(text)%2!=0 or len(text)<2:
        text=input('Ingrese texto: ')
        
    print(rotacion(text))    
    

main()