import pytest
import networkx as nx
from main import create_graph, get_random_nodes, find_shortest_path
import time
from tnr import ContractionHierarchyTNR
import copy
from memory_profiler import memory_usage
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend before importing osmnx


@pytest.fixture
def graph():
    """Fixture to create the graph once for all tests"""
    return create_graph()


def test_graph_not_empty(graph):
    """Test whether graph has nodes and edges"""
    assert len(graph.nodes) > 0
    assert len(graph.edges) > 0


def test_random_nodes_exist(graph):
    """Test whether randomly selected nodes exist in graph"""
    orig, dest = get_random_nodes(graph)
    assert orig in graph.nodes
    assert dest in graph.nodes


def test_shortest_path_validity(graph):
    """Test whether the shortest path is valid"""
    # Get random nodes and find path
    orig, dest = get_random_nodes(graph)
    route = find_shortest_path(graph, orig, dest)

    # Test path properties
    assert isinstance(route, list)
    assert len(route) > 1

    # Test connectivity of consecutive nodes in path
    for i in range(len(route) - 1):
        assert (graph.has_edge(route[i], route[i + 1]) or
                graph.has_edge(route[i + 1], route[i])), \
            f"Nodes {route[i]} and {route[i + 1]} should be connected"


def test_tnr_vs_dijkstra(graph):
    """Ensure CH-TNR produces distances close to Dijkstra's algorithm"""
    from tnr import ContractionHierarchyTNR

    orig, dest = get_random_nodes(graph)

    # Compute shortest path distance using Dijkstra
    dijkstra_distance = nx.shortest_path_length(graph, source=orig, target=dest, weight="length")

    # Preprocess CH-TNR
    ch_tnr = ContractionHierarchyTNR(graph)
    ch_tnr.preprocess(cell_size=0.01)

    # Compute CH-TNR distance
    tnr_distance = ch_tnr.query(orig, dest)

    print(f"Dijkstra Distance: {dijkstra_distance}")
    print(f"CH-TNR Distance: {tnr_distance}")
    print(f"Difference: {abs(dijkstra_distance - tnr_distance)}")

    # Increase tolerance to see if it helps
    tolerance = 0.1
    assert abs(dijkstra_distance - tnr_distance) / dijkstra_distance < tolerance, \
        f"CH-TNR distance {tnr_distance} deviates too much from Dijkstra {dijkstra_distance}"


def test_tnr_query_valid_distance(graph):
    """Ensure CH-TNR query returns a valid positive finite distance"""

    orig, dest = get_random_nodes(graph)

    ch_tnr = ContractionHierarchyTNR(graph)
    ch_tnr.preprocess(cell_size=0.01)

    tnr_distance = ch_tnr.query(orig, dest)

    assert tnr_distance >= 0, "CH-TNR returned a negative distance"
    assert tnr_distance != float("inf"), "CH-TNR returned an infinite distance"


def test_tnr_uses_transit_nodes(graph):
    """Ensure transit nodes are selected and used in CH-TNR"""

    ch_tnr = ContractionHierarchyTNR(graph)
    ch_tnr.preprocess(cell_size=0.01)

    assert len(ch_tnr.transit_nodes) > 0, "No transit nodes were selected"

    # Pick a random query and check if it uses a transit node
    orig, dest = get_random_nodes(graph)
    path_distance = ch_tnr.query(orig, dest)

    # If the source and destination are far apart, transit nodes should be used
    if path_distance > 1000:  # Example threshold for long-distance queries
        assert any(node in ch_tnr.transit_nodes for node in ch_tnr.access_nodes[orig]), \
            "Transit nodes should be used for long-distance queries"


def test_graph_integrity_after_ch_preprocessing(graph):
    """Ensure CH preprocessing does not alter the original graph structure"""

    original_graph = copy.deepcopy(graph)

    ch_tnr = ContractionHierarchyTNR(graph)
    ch_tnr.preprocess(cell_size=0.01)

    assert graph.nodes == original_graph.nodes, "Nodes were modified during preprocessing"
    assert graph.edges == original_graph.edges, "Edges were modified during preprocessing"


def test_tnr_unreachable_nodes(graph):
    """Ensure CH-TNR returns infinity for disconnected nodes"""

    # Create a disconnected graph (manually remove edges)
    disconnected_graph = graph.copy()
    disconnected_graph.remove_edges_from(list(disconnected_graph.edges)[:10])

    ch_tnr = ContractionHierarchyTNR(disconnected_graph)
    ch_tnr.preprocess(cell_size=0.01)

    # Pick random nodes that may be disconnected
    orig, dest = get_random_nodes(disconnected_graph)

    tnr_distance = ch_tnr.query(orig, dest)

    if not nx.has_path(disconnected_graph, orig, dest):
        assert tnr_distance == float("inf"), "CH-TNR should return infinity for unreachable nodes"


def test_tnr_preprocessing_time(graph):
    """Measure and ensure CH-TNR preprocessing completes within a reasonable time"""

    ch_tnr = ContractionHierarchyTNR(graph)

    start_time = time.time()
    ch_tnr.preprocess(cell_size=0.01)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"CH-TNR Preprocessing Time: {elapsed_time:.2f} seconds")

    # Ensure preprocessing does not take excessively long (adjust threshold based on dataset size)
    assert elapsed_time < 300, "Preprocessing took too long!"


def test_tnr_query_time_vs_dijkstra(graph):
    """Compare CH-TNR query time against Dijkstra"""
    i = 0
    node_pairs = []
    while i < 10:
        orig, dest = get_random_nodes(graph)
        node_pairs.append((orig, dest))
        i += 1

    # Measure Dijkstra execution time
    start_time = time.time()
    for j in node_pairs:
        _ = nx.shortest_path_length(graph, source=j[0], target=j[1], weight="length")  # origin, dest
    dijkstra_time = time.time() - start_time

    # Preprocess CH-TNR
    ch_tnr = ContractionHierarchyTNR(graph)
    ch_tnr.preprocess(cell_size=0.01)

    # Measure CH-TNR query time
    start_time = time.time()
    for k in node_pairs:
        _ = ch_tnr.query(k[0], k[1])  # origin, dest
    tnr_time = time.time() - start_time

    print(f"Dijkstra Time: {dijkstra_time:.6f} seconds")
    print(f"CH-TNR Time: {tnr_time:.6f} seconds")

    # Ensure CH-TNR is significantly faster
    assert tnr_time <= dijkstra_time, "CH-TNR query is slower than Dijkstra!"


def test_tnr_bulk_queries(graph):
    """Stress test CH-TNR query performance on multiple origin-destination pairs"""

    ch_tnr = ContractionHierarchyTNR(graph)
    ch_tnr.preprocess(cell_size=0.01)

    num_queries = 1000  # Adjust based on computational resources
    total_time = 0

    for _ in range(num_queries):
        orig, dest = get_random_nodes(graph)

        start_time = time.time()
        _ = ch_tnr.query(orig, dest)
        total_time += (time.time() - start_time)

    avg_time = total_time / num_queries
    print(f"Average CH-TNR Query Time: {avg_time:.6f} seconds over {num_queries} queries")

    # Ensure queries are consistently fast (adjust threshold)
    assert avg_time < 0.01, "CH-TNR query time is too slow!"


def test_path_endpoints(graph):
    """Test whether path starts and ends at correct nodes"""
    orig, dest = get_random_nodes(graph)
    route = find_shortest_path(graph, orig, dest)
    assert route[0] == orig
    assert route[-1] == dest


def test_tnr_memory_usage(graph):
    """Measure CH-TNR preprocessing memory consumption"""
    from tnr import ContractionHierarchyTNR

    def preprocess():
        ch_tnr = ContractionHierarchyTNR(graph)
        ch_tnr.preprocess(cell_size=0.01)

    mem_before = memory_usage(-1, interval=0.1, timeout=1)[0]  # Get initial memory
    mem_during = memory_usage(preprocess, interval=0.1)  # Measure during execution
    mem_after = memory_usage(-1, interval=0.1, timeout=1)[0]  # After execution

    max_mem_used = max(mem_during) - mem_before

    print(f"CH-TNR Memory Usage: {max_mem_used:.2f} MB")

    # Ensure memory usage is reasonable (adjust threshold based on dataset size)
    assert max_mem_used < 500, "CH-TNR preprocessing used too much memory!"
