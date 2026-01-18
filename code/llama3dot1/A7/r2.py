def fib_rekursiv(n):
    if n <= 0:
        return "Fibonacci-Sequenz beginnt bei n=1"
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fib_rekursiv(n-1) + fib_rekursiv(n-2)
    
def fib_iterativ(n):
    if n <= 0:
        return "Fibonacci-Sequenz beginnt bei n=1"
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n):
        a, b = b, a + b
    
    return b

def fib_memo(n):
    memo = {0: 0, 1: 1}
    
    def fib_helper(k):
        if k not in memo:
            memo[k] = fib_helper(k-1) + fib_helper(k-2)
        return memo[k]
    
    return fib_helper(n)

print(fib_rekursiv(10))  # Fibonacci-Sequenz bis zur 10. Zahl (rekursiv)
print(fib_iterativ(10))  # Fibonacci-Sequenz bis zur 10. Zahl (iterativ)
print(fib_memo(10))      # Fibonacci-Sequenz bis zur 10. Zahl (mit Memoization)