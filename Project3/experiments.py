# Irving Reyes Bravo
# Project 3

import karger
import metrics
import graph_utils


def run_experiment(strategy, num_nodes=1000, num_edges=20000, num_trials=5000):
    graph = graph_utils.generate_random_graph(num_nodes, num_edges)
    true_min_cut = karger.karger_min_cut(graph, 'uniform')  # Baseline for comparison

    cut_sizes = []
    runtimes = []

    for _ in range(num_trials):
        timer = metrics.Timer()
        timer.start()
        cut_size = karger.karger_min_cut(graph, strategy)
        timer.stop()

        cut_sizes.append(cut_size)
        runtimes.append(timer.elapsed())

    min_cut_prob = metrics.calculate_min_cut_probability(cut_sizes, true_min_cut)
    avg_cut_size = metrics.calculate_average_cut_size(cut_sizes)
    runtime_stats = metrics.calculate_runtime_stats(runtimes)

    print(f"Strategy: {strategy}")
    print(f"Min-Cut Probability: {min_cut_prob}")
    print(f"Average Cut Size: {avg_cut_size}")
    print(f"Runtime Stats: {runtime_stats}\n")
