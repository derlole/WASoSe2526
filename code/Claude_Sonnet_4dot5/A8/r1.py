"""
Primzahlfinder mit Sieve of Eratosthenes
Findet alle Primzahlen bis zur n-ten Zahl effizient.
"""

def sieve_of_eratosthenes(n):
    """
    Findet alle Primzahlen bis n mit dem Sieb des Eratosthenes.
    
    Args:
        n (int): Obergrenze (inklusive) für die Primzahlsuche
        
    Returns:
        list: Liste aller Primzahlen bis n
        
    Time Complexity: O(n log log n)
    Space Complexity: O(n)
    """
    if n < 2:
        return []
    
    # Initialisiere boolean Array - True bedeutet "möglicherweise prim"
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False  # 0 und 1 sind keine Primzahlen
    
    # Sieb-Algorithmus
    p = 2
    while p * p <= n:
        if is_prime[p]:
            # Markiere alle Vielfachen von p als nicht-prim
            # Optimierung: Starte bei p*p, da kleinere Vielfache bereits markiert wurden
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1
    
    # Sammle alle Primzahlen
    primes = [num for num in range(2, n + 1) if is_prime[num]]
    return primes


def sieve_of_eratosthenes_optimized(n):
    """
    Optimierte Version des Siebs für sehr große n.
    Verwendet nur ungerade Zahlen (außer 2) um Speicher zu sparen.
    
    Args:
        n (int): Obergrenze (inklusive) für die Primzahlsuche
        
    Returns:
        list: Liste aller Primzahlen bis n
    """
    if n < 2:
        return []
    if n == 2:
        return [2]
    
    # Behandle 2 separat, verwende dann nur ungerade Zahlen
    # Index i repräsentiert die Zahl 2*i + 3
    size = (n - 1) // 2
    is_prime = [True] * size
    
    limit = int(n ** 0.5)
    for i in range((limit - 1) // 2):
        if is_prime[i]:
            p = 2 * i + 3
            # Markiere Vielfache von p
            # Starte bei p*p, da kleinere bereits markiert wurden
            start = (p * p - 3) // 2
            for j in range(start, size, p):
                is_prime[j] = False
    
    # Erstelle Ergebnisliste
    primes = [2]
    primes.extend([2 * i + 3 for i in range(size) if is_prime[i]])
    return primes


def count_primes(n):
    """
    Zählt die Anzahl der Primzahlen bis n (ohne sie alle zu speichern).
    Nützlich für sehr große n.
    
    Args:
        n (int): Obergrenze (inklusive)
        
    Returns:
        int: Anzahl der Primzahlen bis n
    """
    if n < 2:
        return 0
    
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    p = 2
    while p * p <= n:
        if is_prime[p]:
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1
    
    return sum(is_prime)


def print_primes_formatted(primes, columns=10):
    """
    Gibt Primzahlen formatiert aus.
    
    Args:
        primes (list): Liste der Primzahlen
        columns (int): Anzahl der Spalten für die Ausgabe
    """
    if not primes:
        print("Keine Primzahlen gefunden.")
        return
    
    print(f"Gefundene Primzahlen: {len(primes)}\n")
    
    for i, prime in enumerate(primes, 1):
        print(f"{prime:6}", end="")
        if i % columns == 0:
            print()
    
    if len(primes) % columns != 0:
        print()


def main():
    """
    Hauptfunktion mit Beispielen und Benchmarks.
    """
    import time
    
    print("=" * 60)
    print("PRIMZAHLFINDER - Sieve of Eratosthenes")
    print("=" * 60)
    
    # Beispiel 1: Kleine Zahl
    print("\n1. Primzahlen bis 50:")
    print("-" * 60)
    primes_50 = sieve_of_eratosthenes(50)
    print_primes_formatted(primes_50)
    
    # Beispiel 2: Mittlere Zahl
    print("\n2. Primzahlen bis 200 (erste und letzte 10):")
    print("-" * 60)
    primes_200 = sieve_of_eratosthenes(200)
    print(f"Erste 10: {primes_200[:10]}")
    print(f"Letzte 10: {primes_200[-10:]}")
    print(f"Gesamt: {len(primes_200)} Primzahlen")
    
    # Beispiel 3: Performance-Test
    test_values = [1_000, 10_000, 100_000, 1_000_000]
    
    print("\n3. Performance-Vergleich:")
    print("-" * 60)
    print(f"{'n':>12} {'Standard (ms)':>15} {'Optimiert (ms)':>16} {'Anzahl Primzahlen':>20}")
    print("-" * 60)
    
    for n in test_values:
        # Standard-Version
        start = time.time()
        primes_std = sieve_of_eratosthenes(n)
        time_std = (time.time() - start) * 1000
        
        # Optimierte Version
        start = time.time()
        primes_opt = sieve_of_eratosthenes_optimized(n)
        time_opt = (time.time() - start) * 1000
        
        print(f"{n:12,} {time_std:14.2f} {time_opt:15.2f} {len(primes_std):19,}")
    
    # Beispiel 4: Interaktive Eingabe
    print("\n4. Eigene Berechnung:")
    print("-" * 60)
    try:
        user_input = input("Gib eine Zahl ein (oder Enter für 100): ").strip()
        n = int(user_input) if user_input else 100
        
        if n < 0:
            print("Bitte gib eine positive Zahl ein.")
        elif n > 10_000_000:
            print(f"Berechne Primzahlen bis {n:,}...")
            start = time.time()
            count = count_primes(n)
            elapsed = (time.time() - start) * 1000
            print(f"Anzahl Primzahlen: {count:,}")
            print(f"Berechnungszeit: {elapsed:.2f} ms")
        else:
            start = time.time()
            primes = sieve_of_eratosthenes(n)
            elapsed = (time.time() - start) * 1000
            
            if len(primes) <= 100:
                print_primes_formatted(primes)
            else:
                print(f"Erste 20: {primes[:20]}")
                print(f"Letzte 20: {primes[-20:]}")
                print(f"\nGesamt: {len(primes):,} Primzahlen")
                print(f"Berechnungszeit: {elapsed:.2f} ms")
                
    except ValueError:
        print("Ungültige Eingabe.")
    except KeyboardInterrupt:
        print("\n\nProgramm abgebrochen.")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()