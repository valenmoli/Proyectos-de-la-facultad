def aBinario(n):
    binario=0
    for i in range(10):
        ubinario=((n//2**i)%2)*10**i
        binario+=ubinario
    return binario
def main():
    n=int(input('Ingrese un numero (menor a 1000):'))
    
    print(aBinario(n))

main()