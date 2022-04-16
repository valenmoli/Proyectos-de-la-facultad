def inserOrdd(l,n):
    for i in range (0,len(l)-1):
        for j in range(i+1,len(l)):
            if l[i]>l[j]:
                aux=l[i]
                l[i]=l[j]
                l[j]=aux 
    
def main():
    l=[]
    nl=int(input('ingrese valor para l: '))
    while nl!=0:
        if l==[]:
            l.append(nl)
        for i in range(0,len(l)):
            if l[i]>=nl:
                
                inserOrdd(l,nl)
            else:
                l.append(nl)
        nl=int(input())
    print(l)            
main()