def estaenlista1(n,l):
    
    return n in l
def estaenlista2(n,l):
    v=False
    for i in l:
        if n==i:
            v=True
    return v
def estaenlista3(n,l):
    i=0
    v2=False
    while i<len(l):
        if l[i]==n:
            v2=True
        i+=1
    return v2
def main():
    lista=[1,2,3,4,5]
    num=2
    
    print(estaenlista3(num,lista))
    
    
main()