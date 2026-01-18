def sieve_of_eratosthenes(n):
    if n < 2:
        return []
    
    # Erstellen eines booleschen Arrays, wobei True bedeutet, dass die Zahl eine Primzahl ist.
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False  # 0 und 1 sind keine Primzahlen
    
    p = 2
    while p * p <= n:
        if is_prime[p]:
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1
    
    # Extrahieren der Primzahlen aus dem booleschen Array
    primes = [num for num, prime in enumerate(is_prime) if prime]
    return primes

# Beispielaufruf
n = int(input("Geben Sie die Grenze n ein: "))
primes = sieve_of_eratosthenes(n)
print(f"Alle Primzahlen bis zur {n}-ten Zahl sind: {primes}")