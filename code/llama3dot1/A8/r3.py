def sieve_of_eratosthenes(n):
    """
    Find all prime numbers up to the n-th number.

    Args:
        n (int): The upper limit of the range.

    Returns:
        list: A list of prime numbers.
    """
    # Erstelle eine Bitmaske mit 'n' Bits, wobei das erste Bit auf 0 gesetzt ist
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False

    # Beginne bei der zweiten Primzahl (2) und markiere alle Vielfachen als nicht prim
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            # Markiere alle Vielfachen von 'i' als nicht prim
            for j in range(i * i, n + 1, i):
                sieve[j] = False

    # Richte eine Liste der Primzahlen ein und füge die tatsächlichen Primzahlen hinzu
    primes = []
    for i in range(2, n + 1):
        if sieve[i]:
            primes.append(i)

    return primes

# Beispiele:
print(sieve_of_eratosthenes(10))  # [2, 3, 5, 7]
print(sieve_of_eratosthenes(20))  # [2, 3, 5, 7, 11, 13, 17, 19]