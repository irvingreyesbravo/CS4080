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


# Recursive Expected Value Policy:
ev_cache = {}


def expected_value(successes, failures):
    if (successes, failures) in ev_cache:
        return ev_cache[(successes, failures)]

    if successes >= 3:
        return 0.5
    if failures >= 3:
        return 0.0

    p_nat1 = 1 / 20
    p_nat20 = 1 / 20
    p_fail = 8 / 20
    p_success = 10 / 20

    ev = (
        p_nat1 * 0 +
        p_nat20 * 0.5 +
        p_fail * expected_value(successes, failures + 1) +
        p_success * expected_value(successes + 1, failures)
    )
    ev_cache[(successes, failures)] = ev
    return ev


def dynamic_policy(successes, failures, rolls):
    return 0.25 >= expected_value(successes, failures)


# Simulation Engine:
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
            return 0.25

        roll = np.random.choice(d20)
        rolls.append(roll)

        if roll == 1:
            return 0
        elif roll == 20:
            return 0.5
        elif roll >= 10:
            successes += 1
            if successes == 3:
                return 0.5
        else:
            failures += 1
            if failures == 3:
                return 0


def summarize(outcomes, label):
    count = Counter(outcomes)
    total = len(outcomes)
    avg_hp = sum(outcomes) / total
    print(f"\n--- {label} ---")
    print(f"Avg HP: {avg_hp:.4f}")
    print(f"Stabilized (0.5): {count[0.5] / total:.2%}")
    print(f"Potion (0.25): {count[0.25] / total:.2%}")
    print(f"Death (0): {count[0] / total:.2%}")
    return {
        'label': label,
        'avg_hp': avg_hp,
        'stabilized': count[0.5] / total,
        'potion': count[0.25] / total,
        'death': count[0] / total
    }


def plot_results(summary_stats):
    labels = [s['label'] for s in summary_stats]
    avg_hp = [s['avg_hp'] for s in summary_stats]
    stabilized = [s['stabilized'] for s in summary_stats]
    potion = [s['potion'] for s in summary_stats]
    death = [s['death'] for s in summary_stats]

    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.bar(x - width, stabilized, width, label='Stabilized (0.5)')
    ax.bar(x, potion, width, label='Potion (0.25)')
    ax.bar(x + width, death, width, label='Death (0)')

    ax.set_ylabel('Proportion of Outcomes')
    ax.set_title('Outcome Distributions by Policy')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15, ha='right')
    ax.legend()
    plt.tight_layout()
    plt.show()

    fig, ax2 = plt.subplots(figsize=(10, 5))
    ax2.bar(labels, avg_hp, color='mediumseagreen')
    ax2.set_ylabel('Average HP')
    ax2.set_title('Average HP Outcome by Policy')
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    plt.show()


def plot_ev_surface():
    states = [(s, f) for s in range(4) for f in range(4) if s < 3 and f < 3]
    evs = [expected_value(s, f) for s, f in states]
    labels = [f"S:{s},F:{f}" for s, f in states]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(labels, evs, color='royalblue')
    ax.axhline(y=0.25, color='red', linestyle='--', label='Potion Value (0.25)')
    ax.set_ylabel('Expected Value of Continuing')
    ax.set_title('Expected Value Across Game States')
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    summary_stats = []
    base_outcomes = simulate(lambda s, f, r: False)
    summary_stats.append(summarize(base_outcomes, "No Potion Policy"))

    p1_outcomes = simulate(policy_after_two_fails)
    summary_stats.append(summarize(p1_outcomes, "Potion After 2 Fails"))

    p2_outcomes = simulate(policy_last_roll)
    summary_stats.append(summarize(p2_outcomes, "Potion on Last Roll"))

    p3_outcomes = simulate(policy_no_successes_after_two_rolls)
    summary_stats.append(summarize(p3_outcomes, "Potion if No Successes After 2 Rolls"))

    p4_outcomes = simulate(dynamic_policy)
    summary_stats.append(summarize(p4_outcomes, "Dynamic EV-Based Policy"))

    plot_results(summary_stats)
    plot_ev_surface()
