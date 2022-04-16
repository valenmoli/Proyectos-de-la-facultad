def ordenarlist(l):
    for i in range (0,len(l)-1):
        for j in range (i+1,len(l)):
            if l[i]>l[j]:
                aux=l[i]
                l[i]=l[j]
                l[j]=aux

    return l

def main():
    n=int(input('Ingrese valor para la lista: '))
    l=[]
    while n!=0:
        l.append(n)
        n=int(input())
    print(ordenarlist(l))
main()
        