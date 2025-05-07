# Irving Reyes Bravo
# Project 3

import experiments
import sys


def main(strategy):
    if strategy not in ['uniform', 'inverse', 'direct']:
        print("Invalid strategy. Choose from: 'uniform', 'inverse', 'direct'.")
        return

    print(f"Running {strategy} bias strategy...")
    experiments.run_experiment(strategy)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <strategy>")
        sys.exit(1)

    selected_strategy = sys.argv[1]
    main(selected_strategy)
