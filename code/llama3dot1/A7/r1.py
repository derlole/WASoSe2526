def fibonacci_rekursiv(n):
    if n <= 1:
        return n
    
    return fibonacci_rekursiv(n-1) + fibonacci_rekursiv(n-2)

def fibonacci_iterativ(n):
    if n <= 1:
        return n
    
    a = 0
    b = 1
    for _ in range(2, n+1):
        c = a + b
        a = b
        b = c
    
    return b

def fibonacci_memo(n, memo={}):
    if n <= 1:
        return n
    
    if n in memo:
        return memo[n]
    
    result = fibonacci_memo(n-1, memo) + fibonacci_memo(n-2, memo)
    memo[n] = result
    
    return result

print(fibonacci_rekursiv(10))  # Rekursive Implementierung
print(fibonacci_iterativ(10))  # Iterative Implementierung
print(fibonacci_memo(10))      # Implementierung mit Memoization