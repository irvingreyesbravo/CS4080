# Irving Reyes Bravo
# Project 3

import matplotlib.pyplot as plt
import numpy as np


def plot_metric(strategy_names, metric_values, metric_name):
    plt.figure(figsize=(10, 6))
    x = np.arange(len(strategy_names))
    plt.bar(x, metric_values, color=['blue', 'orange', 'green'])
    plt.xticks(x, strategy_names)
    plt.xlabel('Strategy')
    plt.ylabel(metric_name)
    plt.title(f'{metric_name} Comparison Across Strategies')
    plt.show()


def plot_runtime_distribution(runtime_data, strategy_names):
    plt.figure(figsize=(10, 6))
    for i, runtime_list in enumerate(runtime_data):
        plt.hist(runtime_list, bins=20, alpha=0.5, label=strategy_names[i])
    plt.xlabel('Runtime (s)')
    plt.ylabel('Frequency')
    plt.title('Runtime Distribution Across Strategies')
    plt.legend()
    plt.show()


def analyze_results(results):
    strategies = list(results.keys())
    min_cut_probs = [results[strategy]['min_cut_prob'] for strategy in strategies]
    avg_cut_sizes = [results[strategy]['avg_cut_size'] for strategy in strategies]
    runtimes = [results[strategy]['runtimes'] for strategy in strategies]

    # Plotting
    plot_metric(strategies, min_cut_probs, 'Min-Cut Probability')
    plot_metric(strategies, avg_cut_sizes, 'Average Cut Size')
    plot_runtime_distribution(runtimes, strategies)
