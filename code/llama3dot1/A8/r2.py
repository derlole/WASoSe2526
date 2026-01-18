def sieve_of_eratosthenes(n):
    """
    Berechnet alle Primzahlen bis zur n-ten Zahl mithilfe des Sieves of Eratosthenes.
    
    Args:
        n (int): Die Anzahl der zu ermittelnden Primzahlen.
    
    Returns:
        list: Eine Liste aller Primzahlen bis zur n-ten Zahl.
    """
    if n < 2:
        return []
    
    # Maximale Grenze für die Primzahlprüfung
    max_limit = int(n ** 0.5) + 1
    
    # Erstelle eine Liste von Booleschen Werten, um zu prüfen, ob ein Zahl prim ist
    sieve = [True] * (n + 1)
    
    # Setze alle ungeraden Zahlen als Primzahl (da jede gerade Zahl außer 2 nicht prim ist)
    for i in range(3, max_limit + 1, 2):
        if sieve[i]:
            k = 2 * i
            while k <= n:
                sieve[k] = False
                k += i
    
    # Setze die Primzahl 2
    sieve[2] = True
    
    # Richte eine Liste mit den Primzahlen ein
    primes = []
    
    # Füge alle primen Zahlen zur Liste hinzu
    for i in range(2, n + 1):
        if sieve[i]:
            primes.append(i)
    
    return primes

# Beispielaufruf:
n = 100
primzahlen = sieve_of_eratosthenes(n)
print("Primzahlen bis zur", n, "-ten Zahl:", primzahlen)