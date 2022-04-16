def positiv(n):
    suma=0
    for i in range(1,n):
        if n%i==0:
            suma+=i

    if suma==n:
        return True
    else:
        return False
def main():
    cant=0
    i=1
    while cant<4:
        if positiv(i):
            cant+=1
            print(i)
        i+=1
main()