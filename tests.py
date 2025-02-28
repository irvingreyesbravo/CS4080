import pytest
import networkx as nx
from main import create_graph, get_random_nodes, find_shortest_path

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
            f"Nodes {route[i]} and {route[i+1]} should be connected"

def test_path_endpoints(graph):
    """Test whether path starts and ends at correct nodes"""
    orig, dest = get_random_nodes(graph)
    route = find_shortest_path(graph, orig, dest)
    assert route[0] == orig
    assert route[-1] == dest