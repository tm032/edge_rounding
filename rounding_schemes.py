from graph import Graph, Matching
import random
import numpy as np

class EdgeRoundingScheme:
    def __init__(self, graph):
        self.graph = graph
        self.matching = Matching(graph)

    def round_next_edge(self):
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def get_matching(self):
        return self.matching.get_matched_edges()
    
    def execute(self, debug=False):
        while len(self.graph.revealed_edges) < len(self.graph.edge_arrival_order) and len(self.matching.get_matched_edges()) < len(self.graph.graph.edges()):
            self.round_next_edge()

        return self.matching.get_matched_edges()
    
    def initialize(self):
        pass


class GreedyRoundingScheme(EdgeRoundingScheme):
    def __init__(self, graph):
        super().__init__(graph)

    def round_next_edge(self):
        edge = self.graph.reveal_next_edge()
        if edge is not None:
            u, v = edge
            if not self.matching.is_matched(u) and not self.matching.is_matched(v):
                self.matching.match(u, v)

class RecursiveRoundingScheme(EdgeRoundingScheme):
    def __init__(self, graph, c=0.5):
        super().__init__(graph)
        self.c = c

    def prob_u_v_unmatched(self, u, v):
        raise NotImplementedError("This method should be implemented by subclasses.")
        
    def round_next_edge(self):
        edge = self.graph.reveal_next_edge()
        if edge is not None:
            u, v = edge
            if not self.matching.is_matched(u) and not self.matching.is_matched(v):
                weight = self.graph.get_edge_weight(u, v)
                matching_probability = weight * self.c / self.prob_u_v_unmatched(u, v)

                if random.random() < matching_probability:
                    self.matching.match(u, v)

class SimpleRecursiveRoundingScheme(RecursiveRoundingScheme):
    def __init__(self, graph, c=0.5):
        super().__init__(graph, c=c)

    def prob_u_v_unmatched(self, u, v):
        prob_u_is_matched = self.c * self.graph.get_incident_edge_weights_sum(u, revealed_only=True)
        prob_v_is_matched = self.c * self.graph.get_incident_edge_weights_sum(v, revealed_only=True)

        return 1 - (prob_u_is_matched + prob_v_is_matched)

class SimulatedRecursiveRoundingScheme(RecursiveRoundingScheme):
    def __init__(self, graph, c=0.5, num_sim_instances=100):
        super().__init__(graph, c=c)
        self.num_sim_instances = num_sim_instances

        # numpy array of Matchings
        self.matching_matrix = np.zeros((num_sim_instances, len(self.graph.graph.nodes())), dtype=bool)
        self.estimated_unmatched_probabilities = {}

        self.max_matching_probability = 0

    def round_next_edge(self):
        edge = self.graph.reveal_next_edge()
        if edge is not None:
            u, v = edge
            # random_vector = np.random.rand(self.num_sim_instances // 2)
            # random_vector = np.concatenate([random_vector, 1 - random_vector]) # Ensure we have a good mix of random values around 0.5

            random_vector = np.random.rand(self.num_sim_instances)

            free_instances = self.get_free_instances(u, v)
            unmatched_probability = max(self.prob_u_v_unmatched(u, v, free_instances), 1e-6) # Avoid division by zero
            weight = self.graph.get_edge_weight(u, v)
            matching_probability = weight * self.c / unmatched_probability

            self.max_matching_probability = max(self.max_matching_probability, matching_probability)
            if matching_probability > 1:
                print(f"Warning: Matching probability {matching_probability} exceeds 1 for edge ({u}, {v}). Capping it at 1.")
                matching_probability = 1

            match_decisions = free_instances & (random_vector < matching_probability)
            self.matching_matrix[:, u] = self.matching_matrix[:, u] | match_decisions
            self.matching_matrix[:, v] = self.matching_matrix[:, v] | match_decisions

            # # Perfectly matched instances are those where (close to) all vertices are matched.
            # perfectly_matched_instances = self.matching_matrix.sum(axis=1)
            # print(f"Edge ({u}, {v}): Estimated unmatched probability = {unmatched_probability:.4f}, Matching probability = {matching_probability:.4f}, Perfectly matched instances = {np.sum(perfectly_matched_instances >= len(self.graph.graph.nodes()) - 1)}")

            if not self.matching.is_matched(u) and not self.matching.is_matched(v):
                weight = self.graph.get_edge_weight(u, v)
                matching_probability = weight * self.c / unmatched_probability

                if random.random() < matching_probability:
                    self.matching.match(u, v)

    def get_free_instances(self, u, v):
        # Take column vector for u and v from the matching_matrix
        u_matched_vector = self.matching_matrix[:, u]
        v_matched_vector = self.matching_matrix[:, v]

        # Determine which instances have both u and v unmatched by checking u & v
        return ~(u_matched_vector | v_matched_vector)

    def prob_u_v_unmatched(self, u, v, free_instances=None):
        if self.graph.get_current_edge() in self.estimated_unmatched_probabilities:
            return self.estimated_unmatched_probabilities[self.graph.get_current_edge()]
        else:
            if free_instances is None:
                free_instances = self.get_free_instances(u, v)
            
            unmatched_count = np.sum(free_instances)

            # if unmatched_count <= self.num_sim_instances * 0.2:
            #     # print(f"Warning: Only {unmatched_count} free instances for edge ({u}, {v}). Probability estimate may be unreliable.")
            #     print(f"Warning: Only {unmatched_count} free instances for edge ({u}, {v}). Probability estimate may be unreliable.")

            self.estimated_unmatched_probabilities[self.graph.get_current_edge()] = unmatched_count / self.num_sim_instances
            return self.estimated_unmatched_probabilities[self.graph.get_current_edge()]
        

    def execute(self, debug=False):
        while len(self.graph.revealed_edges) < len(self.graph.edge_arrival_order) and len(self.matching.get_matched_edges()) < len(self.graph.graph.edges()):
            self.round_next_edge()

        if debug:
            # print(f"Max matching probability observed: {self.max_matching_probability}")
            return self.matching.get_matched_edges(), self.estimated_unmatched_probabilities

        return self.matching.get_matched_edges()
    
    def initialize(self):
        super().initialize()
        self.estimated_unmatched_probabilities = {}
        self.matching_matrix = np.zeros((self.num_sim_instances, len(self.graph.graph.nodes())), dtype=bool)



    



