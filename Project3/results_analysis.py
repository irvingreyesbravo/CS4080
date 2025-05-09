# Irving Reyes Bravo
# Project 3

import visualize


def analyze_and_visualize(all_results):
    strategies = list(all_results.keys())

    # Collect data for box plots
    min_cut_probs = [all_results[strategy]['min_cut_probs'] for strategy in strategies]
    avg_cut_sizes = [all_results[strategy]['avg_cut_sizes'] for strategy in strategies]

    # Collect runtime stats for bar chart
    runtimes = [all_results[strategy]['runtime_stats'] for strategy in strategies]

    print("\nGenerating visualizations...\n")

    for strategy, metrics in all_results.items():
        print(f"Strategy: {strategy}")
        print(f"Min-Cut Probabilities: {metrics['min_cut_probs']}")
        print(f"Average Cut Sizes: {metrics['avg_cut_sizes']}")
        print(f"Runtime Stats: {metrics['runtime_stats']}\n")

    # Box plots
    visualize.plot_min_cut_probability_box(strategies, min_cut_probs)
    visualize.plot_average_cut_size_box(strategies, avg_cut_sizes)

    # Bar chart for runtime stats
    visualize.plot_runtime_stats(strategies, runtimes)
