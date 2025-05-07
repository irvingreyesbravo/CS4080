# Irving Reyes Bravo
# Project 3

import random


def select_edge_uniform(graph):
    edges = list(graph['edges'])
    return random.choice(edges)


def select_edge_inverse(graph):
    edges = list(graph['edges'])
    weights = [1 / weight for _, _, weight in edges]
    total_weight = sum(weights)
    probabilities = [w / total_weight for w in weights]
    return random.choices(edges, probabilities)[0]


def select_edge_direct(graph):
    edges = list(graph['edges'])
    weights = [weight for _, _, weight in edges]
    total_weight = sum(weights)
    probabilities = [w / total_weight for w in weights]
    return random.choices(edges, probabilities)[0]


def contract(graph, edge):
    u, v, _ = edge
    new_edges = []
    for (x, y, weight) in graph['edges']:
        if x == v:
            x = u
        if y == v:
            y = u
        if x != y:
            new_edges.append((x, y, weight))

    new_graph = {
        'vertices': [v for v in graph['vertices'] if v != v],
        'edges': new_edges
    }
    return new_graph


def karger_min_cut(graph, strategy='uniform'):
    while len(graph['vertices']) > 2:
        if strategy == 'uniform':
            edge = select_edge_uniform(graph)
        elif strategy == 'inverse':
            edge = select_edge_inverse(graph)
        elif strategy == 'direct':
            edge = select_edge_direct(graph)
        else:
            raise ValueError("Unknown strategy")
        graph = contract(graph, edge)

    return len(graph['edges'])
