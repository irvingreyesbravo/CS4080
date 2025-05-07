# Irving Reyes Bravo
# Project 3

import random


def generate_random_graph(num_nodes, num_edges):
    edges = set()
    while len(edges) < num_edges:
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u != v:
            weight = random.randint(1, 10)
            edges.add((u, v, weight))

    graph = {
        'vertices': list(range(num_nodes)),
        'edges': list(edges)
    }
    return graph


def load_graph(file_path):
    edges = []
    with open(file_path, 'r') as f:
        for line in f:
            u, v, weight = map(int, line.strip().split())
            edges.append((u, v, weight))

    vertices = set(u for u, v, _ in edges) | set(v for u, v, _ in edges)
    return {'vertices': list(vertices), 'edges': edges}


def get_edge_weights(graph):
    return [weight for _, _, weight in graph['edges']]
