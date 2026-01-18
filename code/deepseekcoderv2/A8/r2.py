def sieve_of_eratosthenes(n):
    if n < 2:
        return []
    
    # Initialize a list to track prime numbers
    is_prime = [True] * (n + 1)
    primes = []
    
    # 0 and 1 are not prime numbers
    is_prime[0], is_prime[1] = False, False
    
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            primes.append(p)
            # Mark multiples of p as not prime
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
    
    # Collect remaining primes
    for p in range(int(n**0.5) + 1, n + 1):
        if is_prime[p]:
            primes.append(p)
    
    return primes

# Example usage:
n = 30  # Find all prime numbers up to the 30th number
primes = sieve_of_eratosthenes(n)
print(f"Prime numbers up to {n}: {primes}")