import random
def cambiaLista(l,a,b):
    for i in len(l):
        if l[i]<a or l[i]>b:
            l.insert(i,random.randint(a,b))
        
    return l
def main():
    n=int(input('Ingrese valor para la lista: '))
    l=[]
    while n!=0:
        if n not in l:
            l.append(n)
            n=int(input())
        else:
            n=int(input())
    a=int(input('Ingrese minimo: '))
    b=int(input('Ingrese máximo: '))

    print(cambiaLista)
main()