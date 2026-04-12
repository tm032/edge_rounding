from graph import Graph, Matching
import random
import numpy as np

SIMPLE_ROUNDING_SCHEME = "SimpleRecursiveRoundingScheme"
SIMULATED_ROUNDING_SCHEME = "SimulatedRecursiveRoundingScheme"
SIMULATED_ROUNDING_SCHEME_WITH_IS = "SimulatedRecursiveRoundingSchemeWithIS"

class EdgeRoundingScheme:
    def __init__(self, graph):
        self.graph = graph
        self.matching = Matching(graph)

    def round_next_edge(self):
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def get_matching(self):
        return self.matching.get_matched_edges()
    
    def execute(self, rng=None):
        if rng is None:
            self.rng = random.Random()
        else:
            self.rng = rng

        return self._execute()

    def _execute(self):
        while len(self.graph.revealed_edges) < len(self.graph.edge_arrival_order) and len(self.matching.get_matched_edges()) < len(self.graph.graph.edges()):
            self.round_next_edge()

        result = {
            "matched_edges": self.matching.get_matched_edges(),
        }

        return result
    
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
                matching_probability = weight * self.c / max(self.prob_u_v_unmatched(u, v), 1e-6) # Avoid division by zero

                if self.rng.random() < matching_probability:
                    self.matching.match(u, v)

class SimpleRecursiveRoundingScheme(RecursiveRoundingScheme):
    def __str__(self):
        return f"SimpleRecursiveRoundingScheme"

    def __init__(self, graph, c=0.5):
        super().__init__(graph, c=c)

    def prob_u_v_unmatched(self, u, v):
        prob_u_is_matched = self.c * self.graph.get_incident_edge_weights_sum(u, revealed_only=True)
        prob_v_is_matched = self.c * self.graph.get_incident_edge_weights_sum(v, revealed_only=True)

        return 1 - (prob_u_is_matched + prob_v_is_matched)

class SimulatedRecursiveRoundingScheme(RecursiveRoundingScheme):
    def __str__(self):
        return f"SimulatedRecursiveRoundingScheme"

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
            random_vector = self.rng.random(self.num_sim_instances)

            free_instances = self.get_free_instances(u, v)
            unmatched_probability = max(self.prob_u_v_unmatched(u, v, free_instances), 1e-10) # Avoid division by zero
            weight = self.graph.get_edge_weight(u, v)

            matching_probability = weight * self.c / unmatched_probability

            self.max_matching_probability = max(self.max_matching_probability, matching_probability)
            if matching_probability > 1:
                print(f"Warning: Matching probability {matching_probability} exceeds 1 for edge ({u}, {v}). Capping it at 1.")
                matching_probability = 1

            match_decisions = free_instances["both"] & (random_vector < matching_probability)
            self.matching_matrix[:, u] = self.matching_matrix[:, u] | match_decisions
            self.matching_matrix[:, v] = self.matching_matrix[:, v] | match_decisions

            if not self.matching.is_matched(u) and not self.matching.is_matched(v):
                weight = self.graph.get_edge_weight(u, v)
                matching_probability = weight * self.c / unmatched_probability

                if self.rng.random() < matching_probability:
                    self.matching.match(u, v)

    def get_free_instances(self, u, v):
        # Take column vector for u and v from the matching_matrix
        u_matched_vector = self.matching_matrix[:, u]
        v_matched_vector = self.matching_matrix[:, v]

        # Determine which instances have both u and v unmatched by checking u & v

        free_instances = {
            "u": ~u_matched_vector, 
            "v": ~v_matched_vector,
            "both": ~(u_matched_vector | v_matched_vector)
        }

        return free_instances

    def prob_u_v_unmatched(self, u, v, free_instances=None):
        if self.graph.get_current_edge() in self.estimated_unmatched_probabilities:
            return self.estimated_unmatched_probabilities[self.graph.get_current_edge()]
        else:
            if free_instances is None:
                free_instances = self.get_free_instances(u, v)

            uv_unmatched_count = np.sum(free_instances["both"])

            unmatched_probability = uv_unmatched_count / self.num_sim_instances

            self.estimated_unmatched_probabilities[self.graph.get_current_edge()] = unmatched_probability
            return self.estimated_unmatched_probabilities[self.graph.get_current_edge()]
        

    def _execute(self):
        while len(self.graph.revealed_edges) < len(self.graph.edge_arrival_order) and len(self.matching.get_matched_edges()) < len(self.graph.graph.edges()):
            self.round_next_edge()

        result = {
            "matched_edges": self.matching.get_matched_edges(),
            "estimated_unmatched_probabilities": self.estimated_unmatched_probabilities
        }

        return result
    
    def initialize(self):
        super().initialize()
        self.estimated_unmatched_probabilities = {}
        self.matching_matrix = np.zeros((self.num_sim_instances, len(self.graph.graph.nodes())), dtype=bool)

    
class SimulatedRecursiveRoundingSchemeWithIS(SimulatedRecursiveRoundingScheme):
    def __str__(self):
        return f"SimulatedRecursiveRoundingSchemeWithIS"

    def __init__(self, graph, average_edge_weight, c=0.5, num_sim_instances=100, r=0.7):
        super().__init__(graph, c=c, num_sim_instances=num_sim_instances)
        self.average_edge_weight = average_edge_weight
        self.weight_vector = np.ones(self.num_sim_instances)
        self.simulation_weight = 1
        self.r = r

    def round_next_edge(self):
        edge = self.graph.reveal_next_edge()
        if edge is not None:
            u, v = edge
            random_vector = self.rng.random(self.num_sim_instances)

            free_instances = self.get_free_instances(u, v)
            weight = self.graph.get_edge_weight(u, v)

            # print(f"Edge ({u}, {v}): weight {weight}, unmatched probability {unmatched_probability}, weight vector: {self.weight_vector}")
            
            target_matching_probability = weight * self.c / max(self.prob_u_v_unmatched(u, v, free_instances, proposal=False), 1e-10)
            proposal_matching_probability = self.average_edge_weight * self.c / max(self.prob_u_v_unmatched(u, v, free_instances, proposal=True), 1e-10)

            proposal_matching_probability = self.r * target_matching_probability + (1 - self.r) * proposal_matching_probability

            self.update_weight_vector(random_vector, target_matching_probability, proposal_matching_probability)


            self.max_matching_probability = max(self.max_matching_probability, proposal_matching_probability)
            if proposal_matching_probability > 1:
                print(f"Warning: Matching probability {proposal_matching_probability} exceeds 1 for edge ({u}, {v}). Capping it at 1.")
                proposal_matching_probability = 1

            match_decisions = free_instances["both"] & (random_vector < proposal_matching_probability)
            self.matching_matrix[:, u] = self.matching_matrix[:, u] | match_decisions
            self.matching_matrix[:, v] = self.matching_matrix[:, v] | match_decisions

            if not self.matching.is_matched(u) and not self.matching.is_matched(v):
                weight = self.graph.get_edge_weight(u, v)
                target_matching_probability = weight * self.c / max(self.prob_u_v_unmatched(u, v, free_instances, proposal=False), 1e-10)
                proposal_matching_probability = self.average_edge_weight * self.c / max(self.prob_u_v_unmatched(u, v, free_instances, proposal=True), 1e-10)
                proposal_matching_probability = self.r * target_matching_probability + (1 - self.r) * proposal_matching_probability

                if self.rng.random() < proposal_matching_probability:
                    self.matching.match(u, v)
                    self.simulation_weight *= target_matching_probability / proposal_matching_probability
                else:
                    self.simulation_weight *= (1 - target_matching_probability) / (1 - proposal_matching_probability)
    
    def update_weight_vector(self, random_vector, target_matching_probability, proposal_matching_probability):
        acceptance_weight = target_matching_probability / proposal_matching_probability
        rejection_weight = (1 - target_matching_probability) / (1 - proposal_matching_probability)

        accepted_indices = random_vector < target_matching_probability
        self.weight_vector[accepted_indices] *= acceptance_weight
        self.weight_vector[~accepted_indices] *= rejection_weight

    def get_free_instances(self, u, v):
        # Take column vector for u and v from the matching_matrix
        u_matched_vector = self.matching_matrix[:, u]
        v_matched_vector = self.matching_matrix[:, v]

        # Determine which instances have both u and v unmatched by checking u & v

        free_instances = {
            "u": ~u_matched_vector, 
            "v": ~v_matched_vector,
            "both": ~(u_matched_vector | v_matched_vector)
        }

        return free_instances

    def prob_u_v_unmatched(self, u, v, free_instances=None, proposal=False):
        if self.graph.get_current_edge() in self.estimated_unmatched_probabilities:
            return self.estimated_unmatched_probabilities[self.graph.get_current_edge()]
        else:
            if free_instances is None:
                free_instances = self.get_free_instances(u, v)

            uv_unmatched_count = np.sum(free_instances["both"])

            if proposal:
                proposal_unmatched_probability = uv_unmatched_count / self.num_sim_instances
                return proposal_unmatched_probability
            else:
                unmatched_probability = np.dot(free_instances["both"], self.weight_vector) / self.num_sim_instances #np.sum(self.weight_vector)
                self.estimated_unmatched_probabilities[self.graph.get_current_edge()] = unmatched_probability
                return self.estimated_unmatched_probabilities[self.graph.get_current_edge()]
    
    def _execute(self):
        while len(self.graph.revealed_edges) < len(self.graph.edge_arrival_order) and len(self.matching.get_matched_edges()) < len(self.graph.graph.edges()):
            self.round_next_edge()

        result = {
            "matched_edges": self.matching.get_matched_edges(),
            "estimated_unmatched_probabilities": self.estimated_unmatched_probabilities,
            "simulation_weight": self.simulation_weight
        }

        return result
