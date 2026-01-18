def sieve_of_eratosthenes(n):
    # Erstellen Sie eine Liste von True-Werten für jede Zahl bis n (0 und 1 sind keine Primzahlen)
    is_prime = [True] * (n + 1)
    p = 2

    while (p * p <= n):
        # Wenn is_prime[p] noch True ist, dann ist es eine Primzahl
        if is_prime[p]:
            # Markiere alle Vielfachen von p als nicht prim
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1

    # Erstellen Sie eine Liste der Primzahlen bis n
    prime_numbers = [p for p in range(2, n + 1) if is_prime[p]]

    return prime_numbers

# Beispiel: Finde alle Primzahlen bis zur 50. Zahl
n = 50
print(f"Primzahlen bis zur {n}-ten Zahl:")
print(sieve_of_eratosthenes(n))