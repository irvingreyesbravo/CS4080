import osmnx as ox
import networkx as nx
import random
from tnr import CHNode, ContractionHierarchyTNR


# Small sample plot: Falcon

def main():
    G = create_graph()
    orig, dest = get_random_nodes(G)
    route = find_shortest_path(G, orig, dest)

    # Calculate the actual distance of the route found by NetworkX
    nx_distance = calculate_path_length(G, route)
    print(f"NetworkX shortest path distance from {orig} to {dest}: {nx_distance}")

    # Create and preprocess CH-TNR
    ch_tnr = ContractionHierarchyTNR(G)
    ch_tnr.preprocess(cell_size=0.01)  # Adjust cell size based on your graph scale

    # Query
    ch_tnr_distance = ch_tnr.query(orig, dest)
    print(f"CH-TNR distance from {orig} to {dest}: {ch_tnr_distance}")

    # Compare the results
    difference = abs(nx_distance - ch_tnr_distance)
    percent_diff = (difference / nx_distance) * 100 if nx_distance > 0 else 0
    print(f"Absolute difference: {difference:.2f} meters")
    print(f"Percentage difference: {percent_diff:.2f}%")

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
