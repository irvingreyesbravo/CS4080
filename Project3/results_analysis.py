# Irving Reyes Bravo
# Project 3

import visualize


def analyze_and_visualize(all_results):
    strategies = list(all_results.keys())
    min_cut_probs = [all_results[strategy]['min_cut_prob'] for strategy in strategies]
    avg_cut_sizes = [all_results[strategy]['avg_cut_size'] for strategy in strategies]

    # Extract runtime stats
    avg_runtimes = [all_results[strategy]['runtime_stats']['average'] for strategy in strategies]
    min_runtimes = [all_results[strategy]['runtime_stats']['min'] for strategy in strategies]
    max_runtimes = [all_results[strategy]['runtime_stats']['max'] for strategy in strategies]

    print("\nGenerating visualizations...")
    for strategy in strategies:
        print(f"Strategy: {strategy}")
        print(f"Min-Cut Probability: {all_results[strategy]['min_cut_prob']}")
        print(f"Average Cut Size: {all_results[strategy]['avg_cut_size']}")
        print(f"Runtime Stats: {all_results[strategy]['runtime_stats']}\n")

    # Visualizations
    visualize.plot_min_cut_probability(strategies, min_cut_probs)
    visualize.plot_average_cut_size(strategies, avg_cut_sizes)
    visualize.plot_runtime_stats(strategies, avg_runtimes, min_runtimes, max_runtimes)
