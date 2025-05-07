# Irving Reyes Bravo
# Project 3

import experiments
import results_analysis


def main():
    print("Running all strategies...\n")

    # Strategies to test
    strategies = ['uniform', 'direct', 'inverse']

    # Collect metrics for all strategies
    all_results = {}
    for strategy in strategies:
        print(f"Running {strategy} bias strategy...")
        min_cut_prob, avg_cut_size, runtime_stats = experiments.run_experiment(strategy)
        all_results[strategy] = {
            'min_cut_prob': min_cut_prob,
            'avg_cut_size': avg_cut_size,
            'runtime_stats': runtime_stats
        }
        print(f"Strategy: {strategy}")
        print(f"Min-Cut Probability: {min_cut_prob}")
        print(f"Average Cut Size: {avg_cut_size}")
        print(f"Runtime Stats: {runtime_stats}\n")

    print("\nGenerating visualizations...")
    results_analysis.analyze_and_visualize(all_results)


if __name__ == "__main__":
    main()
