def fibonacci_rekursiv(n):
    if n <= 1:
        return n
    else:
        return fibonacci_rekursiv(n-1) + fibonacci_rekursiv(n-2)
    
def fibonacci_iterativ(n):
    fib_sequence = [0, 1]
    for i in range(2, n+1):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    return fib_sequence[:n+1]

def fibonacci_memo(n):
    memo = {0: 0, 1: 1}
    def fib(i):
        if i not in memo:
            memo[i] = fib(i-1) + fib(i-2)
        return memo[i]
    return [fib(i) for i in range(n)]

print(fibonacci_rekursiv(10))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
print(fibonacci_iterativ(10))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
print(fibonacci_memo(10))     # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]