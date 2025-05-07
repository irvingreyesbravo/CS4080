import osmnx as ox
import networkx as nx
import random
import time
import psutil
from tnr import CHNode, ContractionHierarchyTNR


# Small sample plot: Falcon

def main():
    print("=== LOADING GRAPH ===")
    G = create_graph()
    orig, dest = get_random_nodes(G)

    print("\n=== RUNNING BASELINE SHORTEST PATH (DIJKSTRA) ===")
    start_dijkstra = time.time()
    route = find_shortest_path(G, orig, dest)
    end_dijkstra = time.time()

    # Calculate the actual distance of the route found by NetworkX
    nx_distance = calculate_path_length(G, route)
    print(f"NetworkX shortest path distance from {orig} to {dest}: {nx_distance}")

    print(f"Dijkstra's distance from {orig} to {dest}: {nx_distance:.2f} meters")
    print(f"Query time (Dijkstra): {end_dijkstra - start_dijkstra:.6f} seconds")

    print("\n=== RUNNING CH-TNR PREPROCESSING ===")
    ch_tnr = ContractionHierarchyTNR(G)
    start_preprocessing = time.time()
    ch_tnr.preprocess(cell_size=0.01)  # Adjust cell size as needed
    end_preprocessing = time.time()
    print(f"Preprocessing time (CH-TNR): {end_preprocessing - start_preprocessing:.4f} seconds")

    print("\n=== CH-TNR QUERY ===")
    start_query = time.time()
    ch_tnr_distance = ch_tnr.query(orig, dest)
    end_query = time.time()
    print(f"CH-TNR distance from {orig} to {dest}: {ch_tnr_distance:.2f} meters")
    print(f"Query time (CH-TNR): {end_query - start_query:.6f} seconds")

    # Compare the results
    difference = abs(nx_distance - ch_tnr_distance)
    percent_diff = (difference / nx_distance) * 100 if nx_distance > 0 else 0

    print("\n=== SHORTEST PATH COMPARISON ===")
    print(f"From node {orig} to node {dest}")
    print(f"Dijkstra's distance: {nx_distance:.2f} meters")
    print(f"CH-TNR distance:     {ch_tnr_distance:.2f} meters")
    print(f"Absolute difference: {difference:.2f} meters")
    print(f"Relative error:      {percent_diff:.2f}%")

    print("\n=== PERFORMANCE METRICS ===")
    print(f"Preprocessing time (CH-TNR): {end_preprocessing - start_preprocessing:.4f} seconds")
    print(f"Query time (Dijkstra):       {end_dijkstra - start_dijkstra:.6f} seconds")
    print(f"Query time (CH-TNR):         {end_query - start_query:.6f} seconds")

    # Memory usage display
    process = psutil.Process()
    mem_usage = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage: {mem_usage:.2f} MB")

    print("\n=== COMPLEXITY SUMMARY ===")
    print(" - Dijkstra’s algorithm: O(E + V log V)")
    print(" - CH-TNR Preprocessing: High upfront cost (depends on contraction order)")
    print(" - CH-TNR Query:         O(log n) expected (via landmark + overlay graph)")

    return G, orig, dest, route


def calculate_path_length(G, path):
    """
    Calculate the total length of a path in the graph

    Args:
        G: NetworkX graph
        path: List of nodes representing the path

    Returns:
        Total length of the path
    """
    total_length = 0
    for i in range(len(path) - 1):
        # Handle multi-edges by selecting the shortest edge
        if G.has_edge(path[i], path[i + 1]):
            # Find the minimum length among possible edges
            edge_data = G.get_edge_data(path[i], path[i + 1])
            if isinstance(edge_data, dict) and 0 in edge_data:  # Single edge with key 0
                total_length += edge_data[0]['length']
            else:  # Multiple edges, find the one with minimum length
                min_length = float('inf')
                for key in edge_data:
                    if 'length' in edge_data[key] and edge_data[key]['length'] < min_length:
                        min_length = edge_data[key]['length']
                total_length += min_length
    return total_length


def create_graph():
    # Define the place name
    place_name = "Falcon, Colorado, USA"

    # Download the road network for driving
    G = ox.graph_from_place(place_name, network_type="drive")

    # Convert to strongly connected component to ensure paths exist
    largest_cc = max(nx.strongly_connected_components(G), key=len)
    G = G.subgraph(largest_cc).copy()

    return G


def get_random_nodes(G):
    print("Sample nodes/edges and attached data:")
    for node, data in list(G.nodes(data=True))[:10]:
        print(node, data)
    for u, v, data in list(G.edges(data=True))[:10]:
        print(u, v, data)

    # orig, dest = list(G.nodes)[:2]  # Predetermined 2 nodes
    orig, dest = random.choices(list(G.nodes), k=2)  # Choose two nodes randomly

    print(f'Info for OpenStreetMap\n----------\norigin node: {orig}\ndestination node: {dest}')
    return orig, dest


def find_shortest_path(G, orig, dest):
    # Compute the shortest path using Dijkstra's algorithm (built in)
    route = nx.shortest_path(G, source=orig, target=dest, weight="length")

    # Plot the graph with the route highlighted
    ox.plot_graph_route(G, route, route_linewidth=4, route_color="red", node_size=30)

    return route


if __name__ == '__main__':
    main()
