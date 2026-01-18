def fib_recursive(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        sequence = fib_recursive(n - 1)
        sequence.append(sequence[-1] + sequence[-2])
        return sequence

# Example usage
print(fib_recursive(10))

def fib_iterative(n):
    if n <= 0:
        return []
    sequence = [0, 1]
    for i in range(2, n):
        next_value = sequence[-1] + sequence[-2]
        sequence.append(next_value)
    return sequence[:n]

# Example usage
print(fib_iterative(10))

def fib_memoization(n):
    if n <= 0:
        return []
    memo = {0: 0, 1: 1}
    sequence = [0]
    for i in range(1, n):
        sequence.append(memo[i])
        memo[i + 1] = memo[i] + memo[i - 1]
    return sequence

# Example usage
print(fib_memoization(10))

