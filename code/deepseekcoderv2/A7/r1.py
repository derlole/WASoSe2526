def fibonacci_recursive(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        sequence = fibonacci_recursive(n - 1)
        sequence.append(sequence[-1] + sequence[-2])
        return sequence

# Beispielaufruf
print(fibonacci_recursive(10))  # Ausgabe: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

def fibonacci_iterative(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        next_number = sequence[-1] + sequence[-2]
        sequence.append(next_number)
    return sequence

# Beispielaufruf
print(fibonacci_iterative(10))  # Ausgabe: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

def fibonacci_memoization(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = fibonacci_memoization(n - 1, memo)
    next_number = sequence[-1] + sequence[-2]
    sequence.append(next_number)
    memo[n] = sequence
    return sequence

# Beispielaufruf
print(fibonacci_memoization(10))  # Ausgabe: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
