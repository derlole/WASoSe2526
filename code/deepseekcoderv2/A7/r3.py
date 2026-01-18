def fib_recursive(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib_recursive(n - 1) + fib_recursive(n - 2)

# Beispielaufruf
n = 10
print(fib_recursive(n))

def fib_iterative(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Beispielaufruf
n = 10
print(fib_iterative(n))

def fib_memoization(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 0:
        result = 0
    elif n == 1:
        result = 1
    else:
        result = fib_memoization(n - 1, memo) + fib_memoization(n - 2, memo)
    
    memo[n] = result
    return result

# Beispielaufruf
n = 10
print(fib_memoization(n))

import time

def measure_time(func, n):
    start_time = time.time()
    result = func(n)
    end_time = time.time()
    return result, end_time - start_time

# Werte von n testen
ns = [5, 10, 20, 30, 40]
for n in ns:
    print(f"n={n}")
    fib_num, time_recursive = measure_time(fib_recursive, n)
    fib_num, time_iterative = measure_time(fib_iterative, n)
    fib_num, time_memoization = measure_time(fib_memoization, n)
    
    print(f"  Fibonacci-Zahl (rekursiv): {fib_num}, Zeit: {time_recursive:.6f} Sekunden")
    print(f"  Fibonacci-Zahl (iterativ): {fib_num}, Zeit: {time_iterative:.6f} Sekunden")
    print(f"  Fibonacci-Zahl (Memoization): {fib_num}, Zeit: {time_memoization:.6f} Sekunden")