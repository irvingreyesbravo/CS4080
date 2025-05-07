# Irving Reyes Bravo
# Project 3

import karger
import metrics
import graph_utils
import time


def run_experiment(strategy, num_nodes=1000, num_edges=20000, num_trials=100):
    graph = graph_utils.generate_random_graph(num_nodes, num_edges)
    true_min_cut = karger.karger_min_cut(graph, 'uniform')  # Baseline for comparison

    cut_sizes = []
    runtimes = []

    for _ in range(num_trials):
        start_time = time.perf_counter()
        cut_size = karger.karger_min_cut(graph, strategy)
        end_time = time.perf_counter()

        cut_sizes.append(cut_size)
        runtimes.append(end_time - start_time)

    min_cut_prob = metrics.calculate_min_cut_probability(cut_sizes, true_min_cut)
    avg_cut_size = metrics.calculate_average_cut_size(cut_sizes)
    runtime_stats = metrics.calculate_runtime_stats(runtimes)

    # Ensure that we only return three values as expected
    return min_cut_prob, avg_cut_size, runtime_stats
