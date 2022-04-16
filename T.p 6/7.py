def inserOrd(l,n):
    for i in range(0,len(l)):
        if l[i]<n and l[i+1]>n:
            l.insert(i+1,n)
    
    return l
def main():
    l=[]
    nl=int(input('Ingrese num para la list: '))
    while nl !=0:
        if nl>0:
            l.append(nl)
            nl=int(input())
    for i in range (0,len(l)-1):
        for j in range(i+1,len(l)):
            if l[i]>l[j]:
                aux=l[i]
                l[i]=l[j]
                l[j]=aux
    
    num=int(input('Ingrese valor a insertar: '))
    while num<0:
         num=int(input('Ingrese valor a insertar: '))
    
    print(inserOrd(l,num))
            
    
main()