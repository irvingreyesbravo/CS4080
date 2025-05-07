# Irving Reyes Bravo
# Project 3

import matplotlib.pyplot as plt
import numpy as np


def plot_min_cut_probability(strategies, probabilities):
    plt.figure(figsize=(10, 6))
    plt.bar(strategies, probabilities, color=['blue', 'green', 'red'])
    plt.xlabel('Strategy')
    plt.ylabel('Min-Cut Probability')
    plt.title('Min-Cut Probability by Strategy')
    plt.ylim(0, 1)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_average_cut_size(strategies, avg_cut_sizes):
    plt.figure(figsize=(10, 6))
    plt.bar(strategies, avg_cut_sizes, color=['blue', 'green', 'red'])
    plt.xlabel('Strategy')
    plt.ylabel('Average Cut Size')
    plt.title('Average Cut Size by Strategy')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_runtime_stats(strategies, avg_runtimes, min_runtimes, max_runtimes):
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


def generate_plots(data):
    """ Generate all visualizations based on the provided data dictionary. """
    strategies = data['strategy']
    min_cut_probs = data['min_cut_prob']
    avg_cut_sizes = data['avg_cut_size']
    avg_runtimes = data['runtime_avg']
    min_runtimes = data['runtime_min']
    max_runtimes = data['runtime_max']

    # Generate the three plots
    plot_min_cut_probability(strategies, min_cut_probs)
    plot_average_cut_size(strategies, avg_cut_sizes)
    plot_runtime_stats(strategies, avg_runtimes, min_runtimes, max_runtimes)
