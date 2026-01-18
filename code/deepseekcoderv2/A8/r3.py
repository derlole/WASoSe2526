def sieve_of_eratosthenes(n):
    if n < 2:
        return []
    
    # Initialisiere ein boolesches Array mit True, wobei alle Elemente bis auf das erste False sind.
    is_prime = [False] * 2 + [True] * (n - 1)
    
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            # Markiere alle Vielfachen von p als False
            for multiple in range(p*p, n+1, p):
                is_prime[multiple] = False
    
    # Sammle die Indizes der True-Werte im Array
    primes = [p for p in range(n+1) if is_prime[p]]
    return primes

# Beispielaufruf
n = 50
primzahlen = sieve_of_eratosthenes(n)
print(f"Alle Primzahlen bis zur {n}-ten Zahl: {primzahlen}")