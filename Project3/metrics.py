# Irving Reyes Bravo
# Project 3

import time


def calculate_min_cut_probability(results, true_min_cut):
    correct_count = sum(1 for cut in results if cut == true_min_cut)
    return correct_count / len(results)


def calculate_average_cut_size(results):
    return sum(results) / len(results)


def calculate_runtime_stats(runtime_list):
    avg_runtime = sum(runtime_list) / len(runtime_list)
    min_runtime = min(runtime_list)
    max_runtime = max(runtime_list)
    return {
        'average': avg_runtime,
        'min': min_runtime,
        'max': max_runtime
    }


class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()
        self.end_time = None  # Reset end_time on new start

    def stop(self):
        if self.start_time is not None:
            self.end_time = time.time()

    def elapsed(self):
        if self.start_time is None:
            return 0
        elif self.end_time is not None:
            return self.end_time - self.start_time
        else:
            # If stop() hasn't been called, calculate based on current time
            return time.time() - self.start_time
