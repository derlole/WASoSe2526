def sieve_of_eratosthenes(n):
    if n < 2:
        return []

    # Initialize a list to track prime status of numbers from 0 to n
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False  # 0 and 1 are not prime numbers

    p = 2
    while (p * p <= n):
        if is_prime[p]:
            # Marking all multiples of p as non-prime
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1

    # Collecting all prime numbers
    primes = [p for p in range(n + 1) if is_prime[p]]
    return primes

# Example usage:
n = 30
primes_up_to_n = sieve_of_eratosthenes(n)
print(f"All prime numbers up to {n}: {primes_up_to_n}")