# CS4080
Coursework for CS 4080

# **Transit Node Routing with Contraction Hierarchies**  
This project implements and evaluates **Transit Node Routing (TNR)** in combination with **Contraction Hierarchies (CH)** to optimize shortest-path queries on large road networks. The goal is to compare different heuristics for CH preprocessing and assess the efficiency of TNR in terms of query time and memory usage.  

## **Project Overview**  
Shortest-path computations are a fundamental problem in graph-based navigation, particularly in road networks. While **Dijkstra’s algorithm** guarantees optimal results, it is computationally expensive for large graphs. Contraction Hierarchies (CH) improve performance by precomputing shortcuts, and Transit Node Routing (TNR) further enhances query efficiency by precomputing paths between strategically chosen "transit nodes."  
This project systematically explores:  
- **CH with different node ordering heuristics**, including **rank-by-degree** and **edge-difference**.  
- **TNR implementation**, validating its correctness against Dijkstra’s algorithm.  
- **Performance evaluation**, comparing query times and memory overhead between CH and TNR.  

## **Implementation Details**  
The project is structured into three key components:  

### **1. Graph Representation**  
- Uses **`networkx.MultiDiGraph`** to model road networks with multiple directed edges.  
- Supports realistic graphs, enabling comparison of preprocessing and query times.  

### **2. Contraction Hierarchies (CH)**  
- Implements **node contraction** with heuristics to determine the best order of contraction.  
- Generates **shortcut edges** to maintain shortest-path consistency.  

### **3. Transit Node Routing (TNR)**  
- Identifies **highway-like transit nodes** for precomputed long-distance routing.  
- Implements efficient query logic:  
  - If both nodes are close, fallback to CH.  
  - Otherwise, use precomputed transit paths.  

## **Testing and Validation**  
The test suite, implemented with **`pytest`**, verifies correctness, performance, and memory usage. The key tests include:  

- **Correctness Tests:** Ensure that CH and TNR return the same shortest-path distances as Dijkstra.  
- **Performance Tests:** Measure **query time** and **memory footprint** during preprocessing and execution.  
- **Graph Structure Tests:** Validate node ordering and shortcut correctness in CH.  

Additional tools:  
- **`memory_profiler`** tracks memory usage.  
- **`matplotlib`** visualizes graph structures.  

## **How to Run the Tests**  
Clone the repository and install dependencies:  
```bash
git clone https://github.com/IRB3020/CS4080.git
cd CS4080
pip install -r requirements.txt
```  
Run the test suite with:  
```bash
pytest tests.py
```  

## Customization
- To test a different city, change the `place_name` variable in `script.py`:
  ```python
  place_name = "Denver, Colorado, USA"
  ```
- Adjust visualization parameters in `ox.plot_graph_route()` if needed.

## Notes
- The script **automatically runs tests** when executed.
- If using in production, you can disable tests by setting an environment variable:
  ```sh
  export RUN_TESTS=false
  ```

## License
This project is open-source and available for modification.

## **Future Work**  
- Implement dynamic updates to CH and TNR.  
- Extend testing to larger road-network datasets.  
- Investigate hybrid techniques combining CH, TNR, and A*.


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
