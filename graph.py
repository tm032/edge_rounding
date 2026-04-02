import networkx 
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, edge_order, graph=None):
        if graph is not None:
            self.graph = graph
        else:
            self.graph = networkx.Graph()
            self.graph.add_edges_from(edge_order)
            
        self.time = 0
        self.revealed_edges = []
        self.edge_arrival_order = edge_order

    def draw(self):
        print(f"edges: {self.graph.edges(data=True)}")
        print(f"(0,1) in E? {self.graph.has_edge(0, 1)}")
        networkx.draw(self.graph, with_labels=True)
        plt.show()

    
    def set_fractional_matching(self, matching):
        for (u, v), weight in matching.items():
            if self.graph.has_edge(u, v):
                self.graph[u][v]['weight'] = weight

    def set_uniform_fractional_matching(self, weight):
        for u, v in self.graph.edges():
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
        return {edge: self.graph[edge[0]][edge[1]].get('weight', 1) for edge in self.get_incident_edges(vertex, revealed_only)}
    
    def get_incident_edge_weights_sum(self, vertex, revealed_only=True):
        incident_edges = self.get_incident_edges(vertex, revealed_only)
        return sum(self.get_incident_edge_weights(vertex, revealed_only)[edge] for edge in incident_edges)
    
    def get_edge_weight(self, u, v):
        if self.graph.has_edge(u, v):
            return self.graph[u][v].get('weight', 1)
        return None
    
    def __str__(self):
        return str(self.graph.edges(data=True))
    
"""
Matching graph that maintains the integral matching by setting matched edge weights 1 and unmatched edge weights 0. 
"""
class Matching(Graph):
    def __init__(self, graph):
        super().__init__([], graph=graph.graph.copy())
        self.set_uniform_fractional_matching(0) # Initialize all edges with weight 0
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



    
