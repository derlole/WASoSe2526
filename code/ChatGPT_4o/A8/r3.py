def sieve_of_eratosthenes(n):
    """
    Gibt alle Primzahlen bis n zurück.
    """
    if n < 2:
        return []

    # Erstelle ein boolesches Array, das anzeigt, ob eine Zahl prim ist
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= n:
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
        p += 1

    # Sammle alle Primzahlen
    primes = [i for i, prime in enumerate(is_prime) if prime]
    return primes

# Beispiel
n = 100
primes = sieve_of_eratosthenes(n)
print(f"Primzahlen bis {n}: {primes}")
