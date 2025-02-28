import networkx as nx
import heapq
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict

class CHNode:
    def __init__(self, node_id: int, level: int = 0):
        self.id = node_id
        self.level = level
        self.shortcuts: Dict[int, float] = {}  # target_id -> weight

class ContractionHierarchyTNR:
    def __init__(self, graph: nx.Graph, num_access_nodes: int = 2):
        """
        Initialize CH-based TNR with original graph
        
        Args:
            graph: Original NetworkX undirected graph
            num_access_nodes: Number of access nodes to select per cell
        """
        self.original_graph = graph
        self.num_access_nodes = num_access_nodes
        self.nodes: Dict[int, CHNode] = {}
        self.transit_nodes: Set[int] = set()
        self.access_nodes: Dict[int, Set[int]] = defaultdict(set)
        self.distance_table: Dict[Tuple[int, int], float] = {}
        
        # Initialize CH nodes
        for node in graph.nodes():
            self.nodes[node] = CHNode(node)
    
    def preprocess(self, cell_size: float = 1.0):
        """
        Preprocess graph using CH and TNR
        
        Args:
            cell_size: Size of grid cells for TNR partitioning
        """
        # 1. Build Contraction Hierarchy
        self._build_contraction_hierarchy()
        
        # 2. Use CH to identify important nodes as transit nodes
        self._select_transit_nodes_from_ch()
        
        # 3. Compute access nodes using CH
        self._compute_access_nodes()
        
        # 4. Build distance table between transit nodes
        self._build_distance_table()

    def _node_importance(self, node: int) -> float:
        """
        Calculate importance of a node for contraction ordering

        Args:
            node: Node ID to evaluate

        Returns:
            Importance score (higher means more important)
        """
        ch_node = self.nodes[node]

        # Count number of shortcuts that would be added
        neighbors = list(self.original_graph.neighbors(node))

        # If node has few neighbors, we can contract it earlier
        if len(neighbors) <= 1:
            return -1  # Prioritize nodes with few neighbors

        # Limit number of neighbor pairs to check to avoid excessive computation
        max_pairs = min(10, len(neighbors) * (len(neighbors) - 1) // 2)
        pairs_checked = 0
        shortcut_count = 0
        edge_difference = 0

        # Use a more efficient approach to check neighbor pairs
        for i, u in enumerate(neighbors):
            for j, v in enumerate(neighbors[i + 1:], i + 1):
                # Stop if we've checked enough pairs
                if pairs_checked >= max_pairs:
                    break

                pairs_checked += 1

                # Check if both edges (u,node) and (node,v) exist and get their weights
                try:
                    # Direct path through node
                    u_to_node = self.original_graph[u][node][0]['length']
                    node_to_v = self.original_graph[node][v][0]['length']
                    direct_dist = u_to_node + node_to_v
                except (KeyError, IndexError):
                    continue  # Skip if edges don't exist or don't have length

                # Check if there's a shorter path without going through node
                # Instead of computing the full shortest path, just check direct edges
                try:
                    # If u and v are directly connected, use that distance
                    if v in self.original_graph[u]:
                        alt_dist = self.original_graph[u][v][0]['length']
                        if alt_dist <= direct_dist:
                            continue  # No shortcut needed
                except (KeyError, IndexError):
                    pass  # No direct edge, continue with shortcut check

                # If we get here, a shortcut might be necessary
                # We'll add a small penalty for long shortcuts
                shortcut_count += 1
                edge_difference += 1  # Add shortcut

        # Subtract removed edges (more edges removed = more important to contract)
        edge_difference -= len(neighbors)

        # Consider node level in the hierarchy
        level_factor = ch_node.level / 20.0  # Scale down the influence of level

        # Combine factors into importance score
        # Lower importance = contract earlier
        return shortcut_count + edge_difference + level_factor
    
    def _build_contraction_hierarchy(self):
        """
        Build contraction hierarchy by iteratively contracting least important nodes
        """
        remaining_nodes = set(self.nodes.keys())
        current_level = 0
        
        while remaining_nodes:
            # Find least important node
            node_to_contract = min(remaining_nodes, 
                                 key=lambda x: self._node_importance(x))
            
            # Contract node
            self._contract_node(node_to_contract, current_level)
            
            remaining_nodes.remove(node_to_contract)
            current_level += 1
    
    def _contract_node(self, node: int, level: int):
        """
        Contract a node by adding necessary shortcuts
        
        Args:
            node: Node ID to contract
            level: Current contraction level
        """
        ch_node = self.nodes[node]
        ch_node.level = level
        
        neighbors = list(self.original_graph.neighbors(node))
        
        # Add necessary shortcuts
        for i, u in enumerate(neighbors):
            for v in neighbors[i+1:]:
                if u != v:
                    # Check if shortcut is necessary
                                        # Add error handling for missing edges
                    try:
                        # Check if both edges exist
                        if node in self.original_graph[u] and v in self.original_graph[node]:
                            direct_dist = (self.original_graph[u][node][0]['length'] +
                                        self.original_graph[node][v][0]['length'])
                        else:
                            direct_dist = float('inf')  # No direct path through node
                    except KeyError:
                        direct_dist = float('inf')  # No direct path through node
                    
                    # Try to find alternative path without using node
                    try:
                        path = nx.shortest_path(self.original_graph, u, v, weight='length')
                        if node not in path[1:-1]:  # If node is not on shortest path
                            alt_dist = sum(self.original_graph[path[i]][path[i+1]][0]['length'] 
                                         for i in range(len(path)-1))
                            if alt_dist <= direct_dist:
                                continue
                    except nx.NetworkXNoPath:
                        pass
                    
                    # Add shortcut
                    self.nodes[u].shortcuts[v] = direct_dist
                    self.nodes[v].shortcuts[u] = direct_dist
    
    def _select_transit_nodes_from_ch(self):
        """
        Select transit nodes based on CH levels and node importance
        """
        # Select top nodes from CH as transit nodes
        sorted_nodes = sorted(self.nodes.items(), 
                            key=lambda x: x[1].level, 
                            reverse=True)
        
        # Select top 10% of nodes as transit nodes
        num_transit = max(len(self.nodes) // 10, self.num_access_nodes * 2)
        self.transit_nodes = {node_id for node_id, _ in sorted_nodes[:num_transit]}
    
    def _compute_access_nodes(self):
        """
        Compute access nodes for each node using CH structure
        """
        for node in self.nodes:
            # Find closest transit nodes using CH-based search
            distances = self._ch_based_search(node)
            
            # Select closest transit nodes as access nodes
            closest_transit = sorted(
                [(d, t) for t, d in distances.items() if t in self.transit_nodes],
                key=lambda x: x[0]
            )[:self.num_access_nodes]
            
            self.access_nodes[node] = {t for _, t in closest_transit}
    
    def _ch_based_search(self, source: int) -> Dict[int, float]:
        """
        Perform CH-based search from source node
        
        Args:
            source: Source node ID
            
        Returns:
            Dictionary mapping node IDs to distances
        """
        distances = {source: 0.0}
        pq = [(0.0, source)]
        
        while pq:
            dist, node = heapq.heappop(pq)
            
            if dist > distances[node]:
                continue
            
            # Regular edges
            for neighbor in self.original_graph.neighbors(node):
                weight = self.original_graph[node][neighbor][0]['length']
                new_dist = dist + weight
                
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
            
            # Shortcut edges
            ch_node = self.nodes[node]
            for target, weight in ch_node.shortcuts.items():
                new_dist = dist + weight
                
                if target not in distances or new_dist < distances[target]:
                    distances[target] = new_dist
                    heapq.heappush(pq, (new_dist, target))
        
        return distances
    
    def _build_distance_table(self):
        """
        Build distance table between all pairs of transit nodes using CH
        """
        for source in self.transit_nodes:
            distances = self._ch_based_search(source)
            for target in self.transit_nodes:
                if target in distances:
                    self.distance_table[(source, target)] = distances[target]
    
    def query(self, source: int, target: int) -> float:
        """
        Query shortest path distance between two nodes using CH-TNR
        
        Args:
            source: Source node ID
            target: Target node ID
            
        Returns:
            Shortest path distance
        """
        # Local query if nodes share access nodes
        if self.access_nodes[source].intersection(self.access_nodes[target]):
            return self._ch_based_search(source)[target]
        
        # TNR query using access nodes and CH
        min_distance = float('inf')
        source_distances = self._ch_based_search(source)
        target_distances = self._ch_based_search(target)
        
        for s_access in self.access_nodes[source]:
            if s_access not in source_distances:
                continue
            d1 = source_distances[s_access]
            
            for t_access in self.access_nodes[target]:
                if t_access not in target_distances:
                    continue
                if (s_access, t_access) not in self.distance_table:
                    continue
                    
                d2 = self.distance_table[(s_access, t_access)]
                d3 = target_distances[t_access]
                
                total_distance = d1 + d2 + d3
                min_distance = min(min_distance, total_distance)
        
        return min_distance