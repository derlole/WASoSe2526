def sieve_of_eratosthenes(n):
    if n < 2:
        return []

    # Initialize a boolean array to track prime status of numbers
    is_prime = [True] * (n + 1)
    p = 2

    while (p * p <= n):
        # If is_prime[p] is not changed, then it is a prime
        if is_prime[p]:
            # Update all multiples of p to not prime
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1

    # Collecting all prime numbers
    primes = [p for p in range(2, n + 1) if is_prime[p]]
    return primes

# Example usage:
n = 30
print(f"All prime numbers up to {n}: {sieve_of_eratosthenes(n)}")