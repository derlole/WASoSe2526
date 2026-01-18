"""
Primzahlen-Finder mit dem Sieb des Eratosthenes
Findet alle Primzahlen bis zur n-ten Zahl effizient.
"""

def sieve_of_eratosthenes(n):
    """
    Findet alle Primzahlen bis einschließlich n mit dem Sieb des Eratosthenes.
    
    Args:
        n (int): Die obere Grenze (inklusive)
    
    Returns:
        list: Liste aller Primzahlen bis n
    
    Time Complexity: O(n log log n)
    Space Complexity: O(n)
    """
    if n < 2:
        return []
    
    # Erstelle ein Boolean-Array "is_prime[0..n]" und initialisiere
    # alle Einträge als True. Am Ende werden is_prime[i] genau dann
    # True sein, wenn i eine Primzahl ist.
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False  # 0 und 1 sind keine Primzahlen
    
    # Beginne mit der kleinsten Primzahl 2
    p = 2
    while p * p <= n:
        # Wenn is_prime[p] nicht geändert wurde, dann ist es eine Primzahl
        if is_prime[p]:
            # Markiere alle Vielfachen von p als nicht-prim
            # Beginne bei p*p, da kleinere Vielfache bereits markiert wurden
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1
    
    # Sammle alle Zahlen, die als Primzahlen markiert sind
    primes = [i for i in range(n + 1) if is_prime[i]]
    return primes


def sieve_of_eratosthenes_optimized(n):
    """
    Optimierte Version des Siebs des Eratosthenes.
    Behandelt gerade Zahlen separat für bessere Performance.
    
    Args:
        n (int): Die obere Grenze (inklusive)
    
    Returns:
        list: Liste aller Primzahlen bis n
    """
    if n < 2:
        return []
    if n == 2:
        return [2]
    
    # Behandle 2 separat und arbeite nur mit ungeraden Zahlen
    primes = [2]
    
    # Array nur für ungerade Zahlen (spart 50% Speicher)
    # is_prime[i] repräsentiert die Zahl 2*i + 3
    size = (n - 1) // 2
    is_prime = [True] * size
    
    # Iteriere nur über ungerade Zahlen
    for i in range(size):
        if is_prime[i]:
            p = 2 * i + 3
            primes.append(p)
            
            # Markiere Vielfache von p (nur ungerade)
            # Starte bei p*p
            start = (p * p - 3) // 2
            for j in range(start, size, p):
                is_prime[j] = False
    
    return primes


def count_primes(n):
    """
    Zählt die Anzahl der Primzahlen bis n (ohne sie alle zu speichern).
    Speichereffizienter für sehr große n.
    
    Args:
        n (int): Die obere Grenze (inklusive)
    
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


def get_primes_in_range(start, end):
    """
    Findet alle Primzahlen in einem bestimmten Bereich [start, end].
    
    Args:
        start (int): Untere Grenze (inklusive)
        end (int): Obere Grenze (inklusive)
    
    Returns:
        list: Liste aller Primzahlen im Bereich
    """
    if end < 2:
        return []
    
    # Finde alle Primzahlen bis end
    all_primes = sieve_of_eratosthenes(end)
    
    # Filtere nur die im gewünschten Bereich
    return [p for p in all_primes if p >= start]


def display_primes(primes, columns=10):
    """
    Zeigt Primzahlen in einer formatierten Tabelle an.
    
    Args:
        primes (list): Liste der Primzahlen
        columns (int): Anzahl der Spalten in der Ausgabe
    """
    if not primes:
        print("Keine Primzahlen gefunden.")
        return
    
    print(f"\nGefundene Primzahlen: {len(primes)}")
    print("-" * (columns * 8))
    
    for i, prime in enumerate(primes):
        print(f"{prime:6}", end="  ")
        if (i + 1) % columns == 0:
            print()
    
    if len(primes) % columns != 0:
        print()
    print("-" * (columns * 8))


def main():
    """Hauptprogramm mit Beispielen und Tests."""
    
    print("=" * 60)
    print("PRIMZAHLEN-FINDER - Sieb des Eratosthenes")
    print("=" * 60)
    
    # Beispiel 1: Kleine Zahl
    print("\n[Beispiel 1] Primzahlen bis 30:")
    primes = sieve_of_eratosthenes(30)
    display_primes(primes)
    
    # Beispiel 2: Mittlere Zahl
    print("\n[Beispiel 2] Primzahlen bis 100:")
    primes = sieve_of_eratosthenes(100)
    print(f"Anzahl: {len(primes)}")
    print(f"Erste 10: {primes[:10]}")
    print(f"Letzte 10: {primes[-10:]}")
    
    # Beispiel 3: Große Zahl (nur Anzahl)
    print("\n[Beispiel 3] Primzahlen bis 1.000.000:")
    import time
    
    start_time = time.time()
    count = count_primes(1_000_000)
    elapsed = time.time() - start_time
    print(f"Anzahl: {count:,}")
    print(f"Berechnungszeit: {elapsed:.4f} Sekunden")
    
    # Beispiel 4: Optimierte Version
    print("\n[Beispiel 4] Vergleich Standard vs. Optimiert (n=100.000):")
    
    start_time = time.time()
    primes1 = sieve_of_eratosthenes(100_000)
    time1 = time.time() - start_time
    
    start_time = time.time()
    primes2 = sieve_of_eratosthenes_optimized(100_000)
    time2 = time.time() - start_time
    
    print(f"Standard-Version: {time1:.4f} Sekunden ({len(primes1)} Primzahlen)")
    print(f"Optimierte Version: {time2:.4f} Sekunden ({len(primes2)} Primzahlen)")
    print(f"Speedup: {time1/time2:.2f}x")
    
    # Beispiel 5: Bereich
    print("\n[Beispiel 5] Primzahlen zwischen 50 und 100:")
    range_primes = get_primes_in_range(50, 100)
    display_primes(range_primes)
    
    # Interaktiver Modus
    print("\n" + "=" * 60)
    print("INTERAKTIVER MODUS")
    print("=" * 60)
    
    try:
        n = int(input("\nGib eine Zahl n ein (Primzahlen bis n): "))
        
        if n < 0:
            print("Bitte gib eine positive Zahl ein.")
        elif n > 10_000_000:
            print(f"Warnung: {n:,} ist sehr groß. Dies kann einige Zeit dauern...")
            confirm = input("Fortfahren? (j/n): ")
            if confirm.lower() != 'j':
                print("Abgebrochen.")
                return
        
        start_time = time.time()
        
        if n <= 1000:
            # Für kleine n: zeige alle Primzahlen
            primes = sieve_of_eratosthenes_optimized(n)
            elapsed = time.time() - start_time
            display_primes(primes)
        else:
            # Für große n: zeige nur Statistiken
            count = count_primes(n)
            elapsed = time.time() - start_time
            print(f"\nAnzahl der Primzahlen bis {n:,}: {count:,}")
        
        print(f"Berechnungszeit: {elapsed:.4f} Sekunden")
        
    except ValueError:
        print("Ungültige Eingabe. Bitte gib eine ganze Zahl ein.")
    except KeyboardInterrupt:
        print("\n\nProgramm abgebrochen.")


if __name__ == "__main__":
    main()