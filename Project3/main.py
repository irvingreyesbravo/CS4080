# Irving Reyes Bravo
# Project 3 - Main

import experiments
import results_analysis
import numpy as np


def main():
    strategies = ["uniform", "direct", "inverse"]
    all_results = {strategy: {"min_cut_probs": [], "avg_cut_sizes": [], "runtime_stats": []} for strategy in strategies}

    print("\nRunning all strategies...\n")

    num_runs = 5  # Run each strategy multiple times for more data points

    for _ in range(num_runs):
        for strategy in strategies:
            print(f"Running {strategy} bias strategy...")
            min_cut_prob, avg_cut_size, runtime_stats = experiments.run_experiment(strategy)

            # Collecting data for each run
            all_results[strategy]["min_cut_probs"].append(min_cut_prob)
            all_results[strategy]["avg_cut_sizes"].append(avg_cut_size)

            # Collect runtime stats (accumulate averages, mins, and maxes for each run)
            all_results[strategy]["runtime_stats"].append(runtime_stats)

    # Aggregate runtime stats for bar plot (average across runs)
    for strategy in strategies:
        runtime_stats = all_results[strategy]["runtime_stats"]
        avg_runtimes = [run["average"] for run in runtime_stats]
        min_runtimes = [run["min"] for run in runtime_stats]
        max_runtimes = [run["max"] for run in runtime_stats]

        # Calculate overall average, min, max runtime stats for bar plot
        all_results[strategy]["runtime_stats"] = {
            "average": np.mean(avg_runtimes),
            "min": np.min(min_runtimes),
            "max": np.max(max_runtimes)
        }

    # Pass data to results analysis for visualization
    results_analysis.analyze_and_visualize(all_results)


if __name__ == "__main__":
    main()
