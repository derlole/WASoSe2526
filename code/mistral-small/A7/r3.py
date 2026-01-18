def fibonacci_rekursiv(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        sequence = fibonacci_rekursiv(n - 1)
        sequence.append(sequence[-1] + sequence[-2])
        return sequence

# Beispielaufruf
print(fibonacci_rekursiv(10))

def fibonacci_iterativ(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]

# Beispielaufruf
print(fibonacci_iterativ(10))

def fibonacci_memoization(n, memo={}):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n in memo:
        return memo[n]
    else:
        sequence = fibonacci_memoization(n - 1, memo)
        sequence.append(sequence[-1] + sequence[-2])
        memo[n] = sequence
        return sequence

# Beispielaufruf
print(fibonacci_memoization(10))