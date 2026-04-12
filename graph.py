import json
import random
import copy

import networkx 
import matplotlib.pyplot as plt
from scipy.stats import beta

GRAPH_INSTANCE_DIR = "graph_instances/"

class Graph:
    def __init__(self, json_file=None, graph_instance=None, edge_arrival_order=None):
        if graph_instance is not None and edge_arrival_order is not None:
            self.graph = copy.deepcopy(graph_instance.graph)
            self.edge_arrival_order = copy.deepcopy(edge_arrival_order)

        elif json_file is not None:
            with open(GRAPH_INSTANCE_DIR + json_file, "r") as f:
                json_data = json.load(f)

            self.graph = networkx.Graph()
            self.edge_arrival_order = [eval(edge) for edge in json_data["edge_arrival_order"]]

            for edge, weight in json_data["fractional_matching"].items():
                self.graph.add_edge(eval(edge)[0], eval(edge)[1], weight=weight)

        else:
            self.graph = networkx.Graph()
            self.edge_arrival_order = []

        self.time = 0
        self.revealed_edges = []   

    def set_uniform_edge_weights(self, weight):
        print(f"Setting uniform edge weights: {weight}, for edges: {self.graph}")
        for u, v in self.graph.edges():
            self.graph[u][v]['weight'] = weight

    def set_unbalanced_edge_weights(self, a, b, seed=None):
        self.set_uniform_edge_weights(weight=0) # Initialize all edge weights to 0
        for u, v in self.graph.edges():
            remaining_capacity_u = max(1 - self.get_incident_edge_weights_sum(u, revealed_only=False), 0)
            remaining_capacity_v = max(1 - self.get_incident_edge_weights_sum(v, revealed_only=False), 0)
            print(self.get_incident_edge_weights_sum(u, revealed_only=False), self.get_incident_edge_weights_sum(v, revealed_only=False))
            edge_weight = max(beta.rvs(a, b, random_state=seed), 0.1) * min(remaining_capacity_u, remaining_capacity_v)
            
            if edge_weight < 1e-6:
                edge_weight = 0

            if edge_weight > 1 or edge_weight < 0:
                raise ValueError(f"Invalid edge weight: {edge_weight}, remaining_capacity_u: {remaining_capacity_u}, remaining_capacity_v: {remaining_capacity_v}")
            
            self.graph[u][v]['weight'] = edge_weight

    def randomize_edge_arrival_order(self, seed=None):
        if seed is not None:
            random.seed(seed)
        edge_arrival_order = [(u, v) for u, v in self.graph.edges()]
        random.shuffle(edge_arrival_order)
        self.edge_arrival_order = edge_arrival_order

    def export_to_json(self, file_name):
        with open(GRAPH_INSTANCE_DIR + file_name, "w") as f:
            json.dump({
                "fractional_matching": {str(edge): self.graph[edge[0]][edge[1]]['weight'] for edge in self.graph.edges()},
                "edge_arrival_order": [str(edge) for edge in self.edge_arrival_order]
            }, f, indent=4)        

    def draw(self):
        print(f"edges: {self.graph.edges(data=True)}")
        print(f"(0,1) in E? {self.graph.has_edge(0, 1)}")
        networkx.draw(self.graph, with_labels=True)
        plt.show()
    
    def set_custom_edge_weights(self, edge_weights):
        for (u, v), weight in edge_weights.items():
            if self.graph.has_edge(u, v):
                self.graph[u][v]['weight'] = weight

    def get_current_edge(self):
        if self.time == 0:
            return None
        if self.time <= len(self.edge_arrival_order):
            return self.edge_arrival_order[self.time-1]
        return None

    def reveal_next_edge(self):
        if self.time < len(self.edge_arrival_order):
            edge = self.edge_arrival_order[self.time]
            self.revealed_edges.append(edge)
            self.time += 1
            return edge
        return None
    
    def get_incident_edges(self, vertex, revealed_only=True):
        if revealed_only:
            return set(edge for edge in self.revealed_edges[:-1] if vertex in edge)
        else:
            return set(self.graph.edges(vertex))
    
    def get_incident_edge_weights(self, vertex, revealed_only=True):
        return {edge: self.graph[edge[0]][edge[1]]["weight"] for edge in self.get_incident_edges(vertex, revealed_only)}
    
    def get_incident_edge_weights_sum(self, vertex, revealed_only=True):
        incident_edges = self.get_incident_edges(vertex, revealed_only)
        return sum(self.get_incident_edge_weights(vertex, revealed_only)[edge] for edge in incident_edges)
    
    def get_edge_weight(self, u, v):
        if self.graph.has_edge(u, v):
            return self.graph[u][v]["weight"]
        return None
    
    def __str__(self):
        return str(self.graph.edges(data=True))
    
class StarGraph(Graph):
    def __init__(self, num_leaves):
        super().__init__()
        networkx.star_graph(num_leaves, create_using=self.graph)

class CompleteGraph(Graph):
    def __init__(self, num_vertices):
        super().__init__()
        networkx.complete_graph(num_vertices, create_using=self.graph)
    
class BipartiteGraph(Graph):
    def __init__(self, num_left_vertices, num_right_vertices):
        super().__init__()
        networkx.complete_bipartite_graph(num_left_vertices, num_right_vertices, create_using=self.graph)

class TreeGraph(Graph):
    def __init__(self, r, h):
        super().__init__()
        networkx.balanced_tree(r, h, create_using=self.graph)
    

    
"""
Matching graph that maintains the integral matching by setting matched edge weights 1 and unmatched edge weights 0. 
"""
class Matching(Graph):
    def __init__(self, graph_instance):
        print(f" Matching graph with instance: {graph_instance.graph.copy()}")
        super().__init__([], graph_instance=graph_instance, edge_arrival_order=graph_instance.edge_arrival_order)
        self.set_uniform_edge_weights(0) # Initialize all edges with weight 0
        self.matched_edges = set()
        self.matched_vertices = set()

    def is_matched(self, u):
        return u in self.matched_vertices
    
    def match(self, u, v):
        if self.graph.has_edge(u, v):
            self.graph[u][v]['weight'] = 1
            self.matched_edges.add((u, v))
            self.matched_vertices.add(u)
            self.matched_vertices.add(v)
        else:
            raise ValueError(f"Edge ({u}, {v}) does not exist in the graph.")
    
    def get_matched_edges(self):
        return self.matched_edges

    def get_matched_vertices(self):
        return self.matched_vertices




