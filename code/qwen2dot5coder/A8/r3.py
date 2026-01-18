def sieve_of_eratosthenes(n):
    if n < 2:
        return []

    # Initialize a boolean array that indicates whether each number is prime
    is_prime = [True] * (n + 1)
    p = 2

    while (p * p <= n):
        # If is_prime[p] is not changed, then it is a prime
        if is_prime[p]:
            # Updating all multiples of p to not prime
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1

    # Collecting all prime numbers
    prime_numbers = [p for p in range(2, n + 1) if is_prime[p]]
    return prime_numbers

# Example usage:
n = 30  # Change this value to find primes up to the n-th number
primes_up_to_n = sieve_of_eratosthenes(n)
print(f"Prime numbers up to {n}: {primes_up_to_n}")