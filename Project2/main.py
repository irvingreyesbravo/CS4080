# Irving Reyes Bravo
# Project 2
# Modified simulation based on MarkovDeathSaves.py to explore alternative potion use policies
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

d20 = list(range(1, 21))


# Alternative policies:
# If the player has accumulated two failures:
def policy_after_two_fails(successes, failures, rolls):
    # they use a potion to stabilize, avoiding the third failure risk
    return failures == 2


# If the player reaches the final roll without stabilizing:
def policy_last_roll(successes, failures, rolls):
    # they use a potion as a last resort
    return len(rolls) == 2 and not (successes >= 3 or failures >= 3)


# If the player has not achieved any success after two rolls:
def policy_no_successes_after_two_rolls(successes, failures, rolls):
    # they use a potion to mitigate risk
    return len(rolls) == 2 and successes == 0


# Function that simulates each policy 10,000 times
def simulate(policy_fn, iterations=10000):
    outcomes = []
    for _ in range(iterations):
        outcomes.append(run_death_save(policy_fn))

    return outcomes


def run_death_save(policy_fn):
    successes = 0
    failures = 0
    rolls = []

    while True:
        if policy_fn(successes, failures, rolls):
            return 0.25  # potion used, early stabilization

        roll = np.random.choice(d20)
        rolls.append(roll)

        if roll == 1:
            return 0  # nat 1 = death
        elif roll == 20:
            return 0.5  # nat 20 = instant stabilize
        elif roll >= 10:
            successes += 1
            if successes == 3:
                return 0.5
        else:
            failures += 1
            if failures == 3:
                return 0


# Function that displays average HP and outcome rates
def summarize(outcomes, label):
    count = Counter(outcomes)
    total = len(outcomes)
    print(f"\n--- {label} ---")
    print(f"Avg HP: {sum(outcomes) / total:.4f}")
    print(f"Stabilized (0.5): {count[0.5] / total:.2%}")
    print(f"Potion (0.25): {count[0.25] / total:.2%}")
    print(f"Death (0): {count[0] / total:.2%}")
    return sum(outcomes) / total, count


def plot_results(results_dict):
    labels = list(results_dict.keys())
    avg_hp = [v[0] for v in results_dict.values()]
    stabilized = [v[1].get(0.5, 0) / sum(v[1].values()) for v in results_dict.values()]
    potion = [v[1].get(0.25, 0) / sum(v[1].values()) for v in results_dict.values()]
    death = [v[1].get(0.0, 0) / sum(v[1].values()) for v in results_dict.values()]

    x = np.arange(len(labels))
    width = 0.2

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width, stabilized, width, label='Stabilized (0.5)')
    ax.bar(x, potion, width, label='Potion Used (0.25)')
    ax.bar(x + width, death, width, label='Death (0)')

    ax.set_ylabel('Proportion')
    ax.set_title('Death Save Outcomes by Policy')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15)
    ax.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    base_outcomes = simulate(lambda s, f, r: False)  # Never use potion
    summarize(base_outcomes, "No Potion Policy")

    p1_outcomes = simulate(policy_after_two_fails)
    summarize(p1_outcomes, "Policy: Use Potion After Two Fails")

    p2_outcomes = simulate(policy_last_roll)
    summarize(p2_outcomes, "Policy: Use Potion on Last Roll")

    p3_outcomes = simulate(policy_no_successes_after_two_rolls)
    summarize(p3_outcomes, "Policy: Use Potion If No Successes After Two Rolls")

