"""
Fibonacci-Sequenz Implementierung
Verschiedene Ansätze: Rekursiv, Iterativ, Memoization, Generator
"""

import time
from functools import lru_cache


# 1. REKURSIVE IMPLEMENTIERUNG (Einfach, aber ineffizient)
def fibonacci_recursive(n):
    """
    Berechnet die n-te Fibonacci-Zahl rekursiv.
    
    WARNUNG: Sehr ineffizient für n > 35
    Zeitkomplexität: O(2^n)
    Speicherkomplexität: O(n) durch Rekursionsstack
    """
    if n < 0:
        raise ValueError("n muss nicht-negativ sein")
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


# 2. REKURSIV MIT MEMOIZATION (Effizient durch Caching)
@lru_cache(maxsize=None)
def fibonacci_memoized(n):
    """
    Berechnet die n-te Fibonacci-Zahl rekursiv mit Memoization.
    
    Nutzt Python's eingebautes LRU-Cache für optimale Performance.
    Zeitkomplexität: O(n)
    Speicherkomplexität: O(n)
    """
    if n < 0:
        raise ValueError("n muss nicht-negativ sein")
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


# 3. MEMOIZATION MIT EIGENEM DICTIONARY
def fibonacci_memo_dict(n, memo=None):
    """
    Berechnet die n-te Fibonacci-Zahl mit eigenem Memo-Dictionary.
    
    Zeitkomplexität: O(n)
    Speicherkomplexität: O(n)
    """
    if memo is None:
        memo = {}
    
    if n < 0:
        raise ValueError("n muss nicht-negativ sein")
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    
    memo[n] = fibonacci_memo_dict(n - 1, memo) + fibonacci_memo_dict(n - 2, memo)
    return memo[n]


# 4. ITERATIVE IMPLEMENTIERUNG (Optimal für einzelne Werte)
def fibonacci_iterative(n):
    """
    Berechnet die n-te Fibonacci-Zahl iterativ.
    
    Zeitkomplexität: O(n)
    Speicherkomplexität: O(1) - konstanter Speicher!
    """
    if n < 0:
        raise ValueError("n muss nicht-negativ sein")
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


# 5. SEQUENZ GENERIEREN (Iterativ)
def fibonacci_sequence_iterative(n):
    """
    Generiert die komplette Fibonacci-Sequenz bis zur n-ten Zahl.
    
    Returns: Liste mit n+1 Fibonacci-Zahlen [F(0), F(1), ..., F(n)]
    Zeitkomplexität: O(n)
    Speicherkomplexität: O(n)
    """
    if n < 0:
        raise ValueError("n muss nicht-negativ sein")
    
    if n == 0:
        return [0]
    if n == 1:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n + 1):
        sequence.append(sequence[i - 1] + sequence[i - 2])
    
    return sequence


# 6. GENERATOR-IMPLEMENTIERUNG (Speichereffizient für große Sequenzen)
def fibonacci_generator(n):
    """
    Generator für Fibonacci-Zahlen bis zur n-ten Position.
    
    Vorteil: Erzeugt Zahlen on-demand, spart Speicher bei großen n.
    Zeitkomplexität: O(n) gesamt
    Speicherkomplexität: O(1)
    """
    if n < 0:
        raise ValueError("n muss nicht-negativ sein")
    
    a, b = 0, 1
    for i in range(n + 1):
        yield a
        a, b = b, a + b


# 7. MATRIX-EXPONENTATION (Sehr effizient für sehr große n)
def fibonacci_matrix(n):
    """
    Berechnet die n-te Fibonacci-Zahl mit Matrix-Exponentation.
    
    Nutzt die Eigenschaft: [[F(n+1), F(n)], [F(n), F(n-1)]] = [[1,1],[1,0]]^n
    Zeitkomplexität: O(log n)
    Speicherkomplexität: O(log n)
    """
    if n < 0:
        raise ValueError("n muss nicht-negativ sein")
    if n <= 1:
        return n
    
    def matrix_multiply(a, b):
        """Multipliziert zwei 2x2 Matrizen."""
        return [
            [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]
        ]
    
    def matrix_power(matrix, n):
        """Berechnet matrix^n mit schneller Exponentation."""
        if n == 1:
            return matrix
        if n % 2 == 0:
            half = matrix_power(matrix, n // 2)
            return matrix_multiply(half, half)
        else:
            return matrix_multiply(matrix, matrix_power(matrix, n - 1))
    
    base_matrix = [[1, 1], [1, 0]]
    result_matrix = matrix_power(base_matrix, n)
    return result_matrix[0][1]


# HILFSFUNKTIONEN
def benchmark_methods(n):
    """
    Vergleicht die Performance verschiedener Methoden.
    """
    methods = [
        ("Iterativ", fibonacci_iterative),
        ("Memoization (lru_cache)", fibonacci_memoized),
        ("Memoization (dict)", fibonacci_memo_dict),
        ("Matrix-Exponentation", fibonacci_matrix),
    ]
    
    # Nur für kleine n die rekursive Methode testen
    if n <= 35:
        methods.insert(0, ("Rekursiv (LANGSAM)", fibonacci_recursive))
    
    print(f"\n{'='*60}")
    print(f"Performance-Vergleich für n = {n}")
    print(f"{'='*60}")
    
    results = {}
    for name, func in methods:
        start = time.perf_counter()
        result = func(n)
        elapsed = time.perf_counter() - start
        results[name] = (result, elapsed)
        print(f"{name:30s}: {elapsed*1000:8.4f} ms -> F({n}) = {result}")
    
    return results


def print_sequence(n, method="iterative"):
    """
    Gibt die Fibonacci-Sequenz formatiert aus.
    """
    print(f"\nFibonacci-Sequenz bis F({n}):")
    print("-" * 60)
    
    if method == "iterative":
        sequence = fibonacci_sequence_iterative(n)
        for i, fib in enumerate(sequence):
            print(f"F({i:3d}) = {fib:20d}")
    elif method == "generator":
        for i, fib in enumerate(fibonacci_generator(n)):
            print(f"F({i:3d}) = {fib:20d}")


# DEMO UND TESTS
if __name__ == "__main__":
    print("="*60)
    print("FIBONACCI-SEQUENZ IMPLEMENTIERUNGEN")
    print("="*60)
    
    # Test 1: Kleine Sequenz ausgeben
    print("\n1. Kleine Fibonacci-Sequenz (n=10):")
    print_sequence(10)
    
    # Test 2: Einzelne große Zahlen berechnen
    print("\n2. Große Fibonacci-Zahlen:")
    test_values = [50, 100, 500, 1000]
    for n in test_values:
        result = fibonacci_iterative(n)
        print(f"F({n:4d}) = {result}")
    
    # Test 3: Performance-Vergleich
    print("\n3. Performance-Vergleich:")
    benchmark_methods(30)
    
    # Test 4: Generator demonstrieren
    print("\n4. Generator-Beispiel (erste 15 Zahlen):")
    gen_sequence = list(fibonacci_generator(14))
    print(f"Sequenz: {gen_sequence}")
    
    # Test 5: Sehr große Zahlen
    print("\n5. Sehr große Fibonacci-Zahlen:")
    n = 10000
    start = time.perf_counter()
    result = fibonacci_iterative(n)
    elapsed = time.perf_counter() - start
    print(f"F({n}) hat {len(str(result))} Stellen")
    print(f"Berechnungszeit: {elapsed*1000:.4f} ms")
    print(f"Erste 50 Ziffern: {str(result)[:50]}...")
    print(f"Letzte 50 Ziffern: ...{str(result)[-50:]}")
    
    # Test 6: Verifikation der Methoden
    print("\n6. Verifikation (alle Methoden sollten gleiche Ergebnisse liefern):")
    n = 25
    methods = [
        ("Rekursiv", fibonacci_recursive(n)),
        ("Iterativ", fibonacci_iterative(n)),
        ("Memoized", fibonacci_memoized(n)),
        ("Memo-Dict", fibonacci_memo_dict(n)),
        ("Matrix", fibonacci_matrix(n)),
        ("Sequenz", fibonacci_sequence_iterative(n)[n])
    ]
    
    for name, result in methods:
        print(f"{name:15s}: F({n}) = {result}")
    
    print("\n" + "="*60)
    print("Alle Tests abgeschlossen!")
    print("="*60)