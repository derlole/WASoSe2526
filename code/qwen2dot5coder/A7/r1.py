def fibonacci_recursive(n):
    if n <= 0:
        return "Input should be a positive integer."
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

# Beispielaufruf:
print(fibonacci_recursive(10))  # Output: 34
def fibonacci_iterative(n):
    if n <= 0:
        return "Input should be a positive integer."
    elif n == 1:
        return 0
    elif n == 2:
        return 1

    a, b = 0, 1
    for _ in range(2, n):
        a, b = b, a + b
    return b

# Beispielaufruf:
print(fibonacci_iterative(10))  # Output: 34
def fibonacci_memoization(n, memo={}):
    if n <= 0:
        return "Input should be a positive integer."
    elif n in memo:
        return memo[n]
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        memo[n] = fibonacci_memoization(n-1, memo) + fibonacci_memoization(n-2, memo)
        return memo[n]

# Beispielaufruf:
print(fibonacci_memoization(10))  # Output: 34
