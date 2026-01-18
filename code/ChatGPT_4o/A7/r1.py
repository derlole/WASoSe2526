def fibonacci_memoization(n):
    memo = {0: 0, 1: 1}

    def fib(k):
        if k not in memo:
            memo[k] = fib(k-1) + fib(k-2)
        return memo[k]

    return [fib(i) for i in range(n)]

# Beispiel
print("Mit Memoization:", fibonacci_memoization(10))
