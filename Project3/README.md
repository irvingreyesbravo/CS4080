# **Biased Random Edge Selection Strategies in Karger's Min-Cut Algorithm**
This project investigates how introducing biases into the edge selection process affects the performance of **Karger's Min-Cut algorithm**, a randomized algorithm for identifying the minimum cut in a graph. The project implements and evaluates two biased selection strategies—Direct Bias and Inverse Bias—against the traditional uniform random selection approach. The objective is to assess how each strategy impacts runtime, min-cut accuracy, and cut size distribution in a dense, weighted graph structure.

## **Project Overview**
The project examines the effect of biased edge selection on the probability of finding the min-cut in a dense, weighted graph with 20,000 edges. By modifying the edge selection process to prioritize edges based on weight, we explore potential trade-offs in algorithmic accuracy and runtime efficiency.
This project systematically covers:
* **Uniform Random Selection**: Karger's original approach of selecting edges uniformly at random.
* **Direct Bias Strategy**: Prioritizes high-weight edges, potentially increasing runtime while risking incorrect min-cuts.
* **Inverse Bias Strategy**: Prioritizes low-weight edges, aiming to preserve critical edges, increasing the likelihood of finding the true min-cut.
* **Statistical Analysis and Visualization** of min-cut probabilities, average cut sizes, and runtime variability.

## **Implementation Details**
The code is structured as a modular Python framework that includes:
* Three customizable edge selection strategies: Uniform, Direct Bias, and Inverse Bias.
* Iterative algorithm runs to gather statistical data on runtime, cut size, and min-cut probability.
* Confidence interval analysis to provide additional context for runtime variability and cut size distributions.
* Visualization:
  * Min-Cut Probability with confidence intervals.
  * Average Cut Size distribution across strategies.
  * Runtime statistics (min, average, max) across iterations.

## Notes
* The dense graph is generated with 20,000 edges and assigned random weights to simulate realistic network structures.
* Each strategy is run over multiple iterations to aggregate statistics and assess variability.
* Confidence intervals are calculated to provide context for interpreting the stability and reliability of each strategy.
* Dependencies: `numpy`, `matplotlib`, `karger`, and `statistics` (standard library).

## License
This project is open-source and available for modification.

## Future Work
* Explore runtime optimization techniques for the inverse bias strategy to reduce computational overhead.
