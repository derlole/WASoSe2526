"""
Fibonacci-Sequenz Implementierung
Verschiedene Ansätze zur Berechnung der Fibonacci-Zahlen
"""

import time
from functools import lru_cache


def fibonacci_recursive(n):
    """
    Rekursive Implementierung (ineffizient für große n)
    Zeitkomplexität: O(2^n)
    Raumkomplexität: O(n) für Rekursionsstack
    
    Args:
        n: Index der Fibonacci-Zahl (n >= 0)
    
    Returns:
        Die n-te Fibonacci-Zahl
    """
    if n < 0:
        raise ValueError("n muss >= 0 sein")
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n):
    """
    Iterative Implementierung (effizient)
    Zeitkomplexität: O(n)
    Raumkomplexität: O(1)
    
    Args:
        n: Index der Fibonacci-Zahl (n >= 0)
    
    Returns:
        Die n-te Fibonacci-Zahl
    """
    if n < 0:
        raise ValueError("n muss >= 0 sein")
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fibonacci_memoization(n, memo=None):
    """
    Rekursive Implementierung mit Memoization
    Zeitkomplexität: O(n)
    Raumkomplexität: O(n)
    
    Args:
        n: Index der Fibonacci-Zahl (n >= 0)
        memo: Dictionary für gespeicherte Werte
    
    Returns:
        Die n-te Fibonacci-Zahl
    """
    if n < 0:
        raise ValueError("n muss >= 0 sein")
    
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memoization(n - 1, memo) + fibonacci_memoization(n - 2, memo)
    return memo[n]


@lru_cache(maxsize=None)
def fibonacci_lru_cache(n):
    """
    Rekursive Implementierung mit Python's @lru_cache Decorator
    Zeitkomplexität: O(n)
    Raumkomplexität: O(n)
    
    Args:
        n: Index der Fibonacci-Zahl (n >= 0)
    
    Returns:
        Die n-te Fibonacci-Zahl
    """
    if n < 0:
        raise ValueError("n muss >= 0 sein")
    if n <= 1:
        return n
    return fibonacci_lru_cache(n - 1) + fibonacci_lru_cache(n - 2)


def fibonacci_sequence_iterative(n):
    """
    Generiert die komplette Fibonacci-Sequenz bis zur n-ten Zahl
    Zeitkomplexität: O(n)
    Raumkomplexität: O(n)
    
    Args:
        n: Anzahl der Fibonacci-Zahlen (n >= 0)
    
    Returns:
        Liste mit den ersten n Fibonacci-Zahlen
    """
    if n < 0:
        raise ValueError("n muss >= 0 sein")
    if n == 0:
        return []
    if n == 1:
        return [0]
    
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i - 1] + sequence[i - 2])
    return sequence


def fibonacci_generator(n):
    """
    Generator-Funktion für Fibonacci-Sequenz (speichereffizient)
    
    Args:
        n: Anzahl der zu generierenden Fibonacci-Zahlen
    
    Yields:
        Die nächste Fibonacci-Zahl in der Sequenz
    """
    if n < 0:
        raise ValueError("n muss >= 0 sein")
    
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def benchmark_implementations(n):
    """
    Vergleicht die Laufzeit verschiedener Implementierungen
    
    Args:
        n: Index der zu berechnenden Fibonacci-Zahl
    """
    print(f"\n{'='*60}")
    print(f"Benchmark für n = {n}")
    print(f"{'='*60}\n")
    
    implementations = [
        ("Iterativ", fibonacci_iterative),
        ("Memoization", fibonacci_memoization),
        ("LRU Cache", fibonacci_lru_cache),
    ]
    
    # Nur für kleine n rekursiv testen (sehr langsam)
    if n <= 30:
        implementations.insert(0, ("Rekursiv", fibonacci_recursive))
    
    for name, func in implementations:
        start = time.time()
        result = func(n)
        end = time.time()
        print(f"{name:15} | Ergebnis: {result:20} | Zeit: {(end-start)*1000:10.4f} ms")
    
    print(f"\n{'='*60}\n")


def main():
    """
    Hauptfunktion mit Demonstrationen und Tests
    """
    print("FIBONACCI-SEQUENZ IMPLEMENTIERUNGEN")
    print("=" * 60)
    
    # Test 1: Kleine Werte mit allen Methoden
    print("\n1. Test mit kleinen Werten (n=10):")
    n = 10
    print(f"   Rekursiv:     fib({n}) = {fibonacci_recursive(n)}")
    print(f"   Iterativ:     fib({n}) = {fibonacci_iterative(n)}")
    print(f"   Memoization:  fib({n}) = {fibonacci_memoization(n)}")
    print(f"   LRU Cache:    fib({n}) = {fibonacci_lru_cache(n)}")
    
    # Test 2: Sequenz generieren
    print(f"\n2. Fibonacci-Sequenz bis n={n}:")
    print(f"   {fibonacci_sequence_iterative(n)}")
    
    # Test 3: Generator verwenden
    print(f"\n3. Mit Generator (n={n}):")
    print(f"   {list(fibonacci_generator(n))}")
    
    # Test 4: Größere Werte (effiziente Methoden)
    print("\n4. Test mit größeren Werten:")
    large_n = 100
    print(f"   fib({large_n}) = {fibonacci_iterative(large_n)}")
    
    # Test 5: Sehr große Werte
    very_large_n = 1000
    result = fibonacci_iterative(very_large_n)
    print(f"   fib({very_large_n}) = {result}")
    print(f"   (Anzahl Stellen: {len(str(result))})")
    
    # Benchmark
    print("\n5. Performance-Vergleich:")
    benchmark_implementations(30)
    benchmark_implementations(100)
    
    # Interaktiver Modus
    print("\n" + "="*60)
    print("INTERAKTIVER MODUS")
    print("="*60)
    
    while True:
        try:
            user_input = input("\nGib n ein (oder 'q' zum Beenden): ").strip()
            if user_input.lower() == 'q':
                print("Programm beendet.")
                break
            
            n = int(user_input)
            if n < 0:
                print("Fehler: n muss >= 0 sein")
                continue
            
            # Wähle die beste Methode basierend auf n
            if n > 500:
                print(f"\nBerechne fib({n}) mit iterativer Methode...")
                result = fibonacci_iterative(n)
            else:
                print(f"\nBerechne fib({n}) mit LRU Cache...")
                result = fibonacci_lru_cache(n)
            
            print(f"Ergebnis: {result}")
            
            # Zeige Sequenz für kleine n
            if n <= 20:
                show_seq = input("Sequenz anzeigen? (j/n): ").strip().lower()
                if show_seq == 'j':
                    print(f"Sequenz: {fibonacci_sequence_iterative(n)}")
        
        except ValueError:
            print("Fehler: Bitte gib eine gültige Ganzzahl ein.")
        except KeyboardInterrupt:
            print("\n\nProgramm unterbrochen.")
            break
        except Exception as e:
            print(f"Fehler: {e}")


if __name__ == "__main__":
    main()