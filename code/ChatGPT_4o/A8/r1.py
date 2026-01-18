def sieve_of_eratosthenes(n):
    """
    Findet alle Primzahlen bis zur n-ten Zahl (inklusive).
    :param n: int, obere Grenze
    :return: Liste aller Primzahlen <= n
    """
    if n < 2:
        return []

    # Erstelle ein boolsches Array, das angibt, ob die Zahl prim ist
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False  # 0 und 1 sind keine Primzahlen

    p = 2
    while p * p <= n:
        if is_prime[p]:
            # Markiere alle Vielfachen von p als nicht prim
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
        p += 1

    # Alle Zahlen, die True geblieben sind, sind Primzahlen
    primes = [i for i, prime in enumerate(is_prime) if prime]
    return primes


# Beispielnutzung:
n = 100
primzahlen = sieve_of_eratosthenes(n)
print(f"Alle Primzahlen bis {n}:")
print(primzahlen)
