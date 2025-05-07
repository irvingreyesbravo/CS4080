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
