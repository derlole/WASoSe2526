def fibonacci_recursive(n):
    if n <= 0:
        return "Input should be a positive integer."
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

# Example usage:
n = 10
print(f"Fibonacci number at position {n} (recursive): {fibonacci_recursive(n)}")

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

# Example usage:
n = 10
print(f"Fibonacci number at position {n} (iterative): {fibonacci_iterative(n)}")

def fibonacci_memoization(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 0:
        return "Input should be a positive integer."
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    
    memo[n] = fibonacci_memoization(n - 1, memo) + fibonacci_memoization(n - 2, memo)
    return memo[n]

# Example usage:
n = 10
print(f"Fibonacci number at position {n} (memoization): {fibonacci_memoization(n)}")
