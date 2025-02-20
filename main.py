# Kaylee Barcroft
# CS4080 Advanced Algorithms
# Project 1: Contraction Hierarchies and TMR

import osmnx as ox
import networkx as nx
import random
import pytest

# Small sample plot: Falcon

# Define the place name
place_name = "Falcon, Colorado, USA"

# Download the road network for driving
G = ox.graph_from_place(place_name, network_type="drive")

# Visualize the graph (before the shortest path calculations)
# ox.plot_graph(G)

print("Sample nodes/edges and attached data:")
for node, data in list(G.nodes(data=True))[:10]:
    print(node, data)
for u, v, data in list(G.edges(data=True))[:10]:
    print(u, v, data)

# orig, dest = list(G.nodes)[:2]  # Predetermined 2 nodes
orig, dest = random.choices(list(G.nodes), k=2)  # Choose two nodes randomly

print(f'Info for OpenStreetMap\n----------\norigin node: {orig}\ndestination node: {dest}')

# Compute the shortest path using Dijkstra's algorithm (built in)
route = nx.shortest_path(G, source=orig, target=dest, weight="length")

# Plot the graph with the route highlighted
ox.plot_graph_route(G, route, route_linewidth=4, route_color="red", node_size=30)


# Pytests for generated graph
# Irving Reyes Bravo


# Tests whether graph has nodes and edges
def test_graph_not_empty():
    assert len(G.nodes) > 0
    assert len(G.edges) > 0


# Tests whether the origin and destination node exist
def test_random_nodes_exist():
    assert orig in G.nodes
    assert dest in G.nodes


# Tests whether the shortest path is a list with at least 2 nodes
def test_shortest_path_validity():
    assert isinstance(route, list)
    assert len(route) > 1
    for i in range(len(route) - 1):
        assert G.has_edge(route[i], route[i + 1]) or G.has_edge(route[i + 1], route[i]), \
            f"Nodes {route[i]} and {route[i+1]} should be connected"


if __name__ == "__main__":
    pytest.main(["-v"])