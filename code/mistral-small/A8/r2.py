def find_primes(n):
    if n < 2:
        return []

    # Erstellen Sie ein Array, das alle Zahlen bis n repräsentiert und initialisiere es mit True
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False  # 0 und 1 sind keine Primzahlen

    # Verwenden Sie das Sieb des Eratosthenes, um alle nicht-primzahlen zu markieren
    for start in range(2, int(n**0.5) + 1):
        if sieve[start]:
            for multiple in range(start*start, n + 1, start):
                sieve[multiple] = False

    # Extrahieren Sie die Liste der Primzahlen
    primes = [num for num, is_prime in enumerate(sieve) if is_prime]

    return primes

# Beispiel: Finde alle Primzahlen bis zur 100. Zahl
n = 100
primes = find_primes(n)
print(f"Die ersten {n} Primzahlen sind: {primes}")