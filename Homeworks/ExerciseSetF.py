# Name: Randomized Fingerprinting Scheme
# By: Irving Reyes Bravo

import math
import random
import bisect
import matplotlib.pyplot as plt


# Utility: Sieve of Eratosthenes to generate all primes up to max_n^2
def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0:2] = [False, False]
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            is_prime[i * i:limit + 1:i] = [False] * len(range(i * i, limit + 1, i))
    return [i for i, prime in enumerate(is_prime) if prime]


# Step 1: Precompute all primes up to 1000^2
MAX_N = 1000
all_primes = sieve(MAX_N ** 2)

# Step 2: Main analysis loop
theoretical_rates = []
empirical_rates = []
n_values = range(6, MAX_N + 1)
NUM_TRIALS = 10000

for n in n_values:
    lower = n + 1
    upper = n * n
    prime_range = all_primes[bisect.bisect_right(all_primes, lower - 1):bisect.bisect_right(all_primes, upper)]

    # Theoretical K: product of as many primes in the range as possible under 2^n
    max_val = 2 ** n - 1
    k = 1
    k_primes = []
    for p in prime_range:
        if k * p > max_val:
            break
        k *= p
        k_primes.append(p)

    theoretical_fp_rate = len(k_primes) / len(prime_range) if prime_range else 0
    theoretical_rates.append(theoretical_fp_rate)

    # Empirical estimation
    false_positives = 0
    batch = random.choices(prime_range, k=NUM_TRIALS)
    for p in batch:
        if k % p == 0:
            false_positives += 1
    empirical_fp_rate = false_positives / NUM_TRIALS
    empirical_rates.append(empirical_fp_rate)

# Step 3: Plotting
plt.figure(figsize=(12, 6))
plt.plot(n_values, theoretical_rates, label='Theoretical False Positive Rate', color='blue')
plt.plot(n_values, empirical_rates, label='Empirical False Positive Rate', color='orange', alpha=0.7)
plt.xlabel('n (bit-length of x and y)')
plt.ylabel('False Positive Rate')
plt.title('Worst False Positive Rate vs n in Fingerprinting Scheme')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
