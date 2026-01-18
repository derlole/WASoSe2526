def sieve_of_eratosthenes(n):
    # Erstellen Sie ein Array, das alle Zahlen von 0 bis n enthält und es initial mit True (prim) markieren
    is_prime = [True] * (n + 1)
    p = 2

    while (p * p <= n):
        # Wenn is_prime[p] noch wahr ist, dann ist p eine Primzahl
        if (is_prime[p] == True):
            # Updates alle Vielfachen von p
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1

    # Erzeugen Sie eine Liste der Primzahlen bis n
    prime_numbers = [p for p in range(2, n + 1) if is_prime[p]]

    return prime_numbers

# Beispiel: Finde alle Primzahlen bis zur 100. Zahl
n = 100
print("Die ersten", n, "Primzahlen sind:", sieve_of_eratosthenes(n))