# Irving Reyes Bravo
# Project 3

import matplotlib.pyplot as plt
import numpy as np


def plot_min_cut_probability_box(strategies, probabilities):
    plt.figure(figsize=(10, 6))
    plt.boxplot(probabilities, labels=strategies, patch_artist=True,
                boxprops=dict(facecolor='blue', alpha=0.7),
                medianprops=dict(color='black'))
    plt.xlabel('Strategy')
    plt.ylabel('Min-Cut Probability')
    plt.title('Min-Cut Probability Distribution by Strategy')
    plt.ylim(0, 1.1)
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_average_cut_size_box(strategies, avg_cut_sizes):
    plt.figure(figsize=(10, 6))
    plt.boxplot(avg_cut_sizes, labels=strategies, patch_artist=True,
                boxprops=dict(facecolor='green', alpha=0.7),
                medianprops=dict(color='black'))
    plt.xlabel('Strategy')
    plt.ylabel('Average Cut Size')
    plt.title('Average Cut Size Distribution by Strategy')
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_runtime_stats(strategies, runtimes):
    avg_runtimes = [stats['average'] for stats in runtimes]
    min_runtimes = [stats['min'] for stats in runtimes]
    max_runtimes = [stats['max'] for stats in runtimes]

    x = np.arange(len(strategies))
    width = 0.25

    plt.figure(figsize=(12, 7))
    plt.bar(x - width, min_runtimes, width, label='Min Runtime', color='blue')
    plt.bar(x, avg_runtimes, width, label='Avg Runtime', color='green')
    plt.bar(x + width, max_runtimes, width, label='Max Runtime', color='red')

    plt.xlabel('Strategy')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime Statistics by Strategy')
    plt.xticks(ticks=x, labels=strategies, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
