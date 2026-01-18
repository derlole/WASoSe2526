def fibonacci_recursive(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

# Beispielaufruf
n = 10
print(f"Fibonacci-Sequenz bis zur {n}-ten Zahl (rekursiv):")
for i in range(n):
    print(fibonacci_recursive(i), end=" ")
print()

def fibonacci_iterative(n):
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
print(f"Fibonacci-Sequenz bis zur {n}-ten Zahl (iterativ):")
for i in range(n):
    print(fibonacci_iterative(i), end=" ")
print()

def fibonacci_memoization(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        memo[n] = fibonacci_memoization(n-1, memo) + fibonacci_memoization(n-2, memo)
        return memo[n]

# Beispielaufruf
n = 10
print(f"Fibonacci-Sequenz bis zur {n}-ten Zahl (mit Memoization):")
for i in range(n):
    print(fibonacci_memoization(i), end=" ")
print()

