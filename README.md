# CS4080
Coursework for CS 4080
# TNR Program Tool

## Overview
This program downloads a road network graph for a specified location using OpenStreetMap data and computes the shortest path between two randomly selected nodes using **Dijkstra's Algorithm**. The program also visualizes the graph and the computed shortest path.

Additionally, **automated tests** using `pytest` verify the correctness of the graph structure and shortest path calculations.

## Features
- Fetches a road network from **OpenStreetMap** for a specified location.
- Uses **NetworkX** to compute the shortest path based on road lengths.
- Randomly selects two nodes (origin & destination) from the graph.
- Plots the road network and highlights the computed shortest path.
- Runs **pytest** automatically to validate correctness.

## Installation
### Prerequisites
Ensure you have **Python 3.7+** installed along with the following dependencies:
```sh
pip install osmnx networkx matplotlib pytest
```

## Usage
Simply run the script:
```sh
python script.py
```
This will:
1. Download the road network.
2. Compute and display the shortest path.
3. Run the test cases automatically.

## Automated Testing
The script integrates **pytest** to validate core functionalities. The following tests are included:

### Test Cases
| Test Name                 | Description |
|---------------------------|-------------|
| `test_graph_not_empty`    | Ensures the graph has nodes and edges. |
| `test_random_nodes_exist` | Verifies that randomly chosen nodes exist in the graph. |
| `test_shortest_path_validity` | Ensures the computed shortest path is valid and continuous. |

### Running Tests Manually
If you want to run the tests separately, use:
```sh
pytest -v script.py
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
