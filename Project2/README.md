# **D&D Death Save Policy Optimization**  
This project simulates and evaluates different decision-making policies for **Dungeons & Dragons (D&D)** "death saving throws," a probabilistic mechanic used to determine whether a player character survives after falling unconscious. The project models the outcomes of death saves and explores how varying decision policies—especially when and whether to use a stabilizing potion—affect survival and expected recovery. The goal is to compare static heuristics with a dynamic, expected-value-based policy to better understand optimal play under uncertainty.  

## **Project Overview**  
This project explores how different stopping rules impact survival and recovery in a simplified chance-based system derived from D&D's death save rules. A recursive expected-value (EV) model is used to dynamically determine the best action (roll or use potion) based on the player's current state (number of successes and failures). Monte Carlo simulations are run to compare the performance of static and dynamic strategies in terms of average HP, survival rate, and potion usage.
This project systematically covers:  
- **Heuristic-based stopping policies**.  
- **Recursive expected value (EV) modeling** for decision optimization.
- **Monte Carlo simulation techniques** 
- **Visualization of outcome distributions and expected values** across game states.  

## **Implementation Details**
The code is structured as a single Python simulation framework that includes:
- Five customizable policies: including "always roll", "after 2 fails", and a dynamic EV-based strategy
- Recursive expected value computation with memoization
- A simulation engine that runs thousands of trials per policy
- Outcome tracking: survival, potion use, average HP
- Visualization:
  - Outcome distribution bar plots
  - Average HP comparison
  - Expected value surface plot across state space

## Notes
- Each simulation trial models independent rolls of a 20-sided die, per D&D rules.
- The potion provides a fixed HP value of 0.25 and prevents further rolls.
- Dynamic policy decisions are made by comparing expected value of continuing to potion value.
- The EV surface visualization helps explain policy behavior in specific game states.
- Dependencies: `numpy`, `matplotlib`, and `collections` (standard library).

## License
This project is open-source and available for modification.

## Future Work
- Implement weighted dice (e.g., biased D20) to simulate altered probability spaces
- Explore more complex value structures (e.g., scaling potion rewards or HP thresholds)
- Apply reinforcement learning for policy learning instead of hand-crafted EV logic