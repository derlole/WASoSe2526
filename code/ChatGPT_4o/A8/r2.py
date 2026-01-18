def sieve_of_eratosthenes(limit):
    """
    Findet alle Primzahlen bis zur gegebenen Zahl `limit` mit dem Sieve of Eratosthenes.
    """
    if limit < 2:
        return []

    # Initialisiere eine Liste, die angibt, ob eine Zahl prim ist
    is_prime = [True] * (limit + 1)
    is_prime[0], is_prime[1] = False, False  # 0 und 1 sind keine Primzahlen

    # Sieb des Eratosthenes
    for num in range(2, int(limit ** 0.5) + 1):
        if is_prime[num]:
            for multiple in range(num*num, limit + 1, num):
                is_prime[multiple] = False

    # Extrahiere die Primzahlen
    primes = [i for i, prime in enumerate(is_prime) if prime]
    return primes

# Beispielnutzung
n = int(input("Gib die obere Grenze n ein: "))
primes = sieve_of_eratosthenes(n)
print(f"Alle Primzahlen bis {n}:")
print(primes)
