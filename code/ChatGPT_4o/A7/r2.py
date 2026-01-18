# Fibonacci-Sequenz Berechnung

# 1️⃣ Rekursiver Ansatz (nicht effizient für große n)
def fibonacci_recursive(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    seq = fibonacci_recursive(n - 1)
    seq.append(seq[-1] + seq[-2])
    return seq

# 2️⃣ Iterativer Ansatz (effizient für große n)
def fibonacci_iterative(n):
    if n <= 0:
        return []
    seq = [0, 1]
    for i in range(2, n):
        seq.append(seq[-1] + seq[-2])
    return seq[:n]

# 3️⃣ Memoization / Dynamische Programmierung (rekursiv + Cache)
def fibonacci_memoization(n):
    memo = {0: 0, 1: 1}

    def fib(k):
        if k not in memo:
            memo[k] = fib(k - 1) + fib(k - 2)
        return memo[k]

    return [fib(i) for i in range(n)]

# ✅ Test der Funktionen
if __name__ == "__main__":
    n = 20  # Beispiel: bis zur 20. Fibonacci-Zahl

    print("Rekursiv:", fibonacci_recursive(n))
    print("Iterativ:", fibonacci_iterative(n))
    print("Memoization:", fibonacci_memoization(n))
