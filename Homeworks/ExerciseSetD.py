# Name: Linear Search Empirical Verification
# By: Irving Reyes Bravo

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


# Function that returns the (i)ndex of the first occurrence of K in A
def linear_search(A, given_K):
    for i, val in enumerate(A):
        if val == given_K:

            return i
    # Or -1 if not found
    return -1


# Function that computes theoretical probabilities for each index i and for not being found (-1)
def compute_probabilities(given_M, given_n):
    p = [(1 - 1 / given_M) ** i * (1 / given_M) for i in range(given_n)]
    p_not_found = 1 - sum(p)
    return p + [p_not_found]


# Function that computes empirical frequencies by running linear search on randomly generated arrays
def compute_frequencies(given_M, given_n, given_K, given_samples=10000):
    alphabet = [chr(65 + i) for i in range(given_M)]
    counts = Counter()

    for _ in range(given_samples):
        A = np.random.choice(alphabet, given_n)
        index = linear_search(A, given_K)
        counts[index] += 1

    total = sum(counts.values())
    return [counts[i] / total for i in range(given_n)] + [counts[-1] / total]


# Set problem parameters:
# Alphabet size
M = 10
# Search key
K = 'I'
# Arrays of different sizes
n_values = [5, 10, 20, 50]
# Number of random arrays per n
num_samples = 100000

# Run problem experiment:
plt.figure(figsize=(10, 6))
for n in n_values:
    theoretical = compute_probabilities(M, n)
    empirical = compute_frequencies(M, n, K, num_samples)

    # X-axis Labels
    indices = list(range(n)) + [-1]
    plt.scatter(indices, empirical, label=f'Empirical (n={n})', marker='o')
    plt.scatter(indices, theoretical, label=f'Theoretical (n={n})', marker='x')

plt.yscale('log')
plt.xlabel("Index in array (or -1 for not found)")
plt.ylabel("Probability")
plt.title("Empirical vs Theoretical Probabilities for Linear Search")
plt.legend()
plt.show()
