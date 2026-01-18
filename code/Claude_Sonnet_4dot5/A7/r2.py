"""
Test-Suite für Fibonacci-Implementierungen
"""

import unittest
from fibonacci import (
    fibonacci_recursive,
    fibonacci_iterative,
    fibonacci_memoization,
    fibonacci_lru_cache,
    fibonacci_matrix,
    fibonacci_sequence,
    fibonacci_generator
)


class TestFibonacciImplementations(unittest.TestCase):
    """Tests für alle Fibonacci-Implementierungen"""
    
    KNOWN_VALUES = [
        (0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5),
        (6, 8), (7, 13), (8, 21), (9, 34), (10, 55),
        (15, 610), (20, 6765), (25, 75025), (30, 832040),
    ]
    
    def test_iterative_known_values(self):
        """Test iterative Implementierung mit bekannten Werten"""
        for n, expected in self.KNOWN_VALUES:
            with self.subTest(n=n):
                self.assertEqual(fibonacci_iterative(n), expected)
    
    def test_consistency_across_methods(self):
        """Teste, dass alle Methoden die gleichen Ergebnisse liefern"""
        test_values = [0, 1, 5, 10, 20, 30]
        
        for n in test_values:
            with self.subTest(n=n):
                expected = fibonacci_iterative(n)
                
                if n <= 30:
                    self.assertEqual(fibonacci_recursive(n), expected)
                
                self.assertEqual(fibonacci_memoization(n), expected)
                self.assertEqual(fibonacci_lru_cache(n), expected)
                self.assertEqual(fibonacci_matrix(n), expected)
    
    def test_large_values(self):
        """Teste große n-Werte"""
        for n in [50, 100, 500]:
            result_iterative = fibonacci_iterative(n)
            result_matrix = fibonacci_matrix(n)
            self.assertEqual(result_iterative, result_matrix)
            self.assertGreater(result_iterative, 0)
    
    def test_negative_input(self):
        """Teste Fehlerbehandlung für negative Eingaben"""
        with self.assertRaises(ValueError):
            fibonacci_iterative(-1)


if __name__ == "__main__":
    unittest.main()