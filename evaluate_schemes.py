from graph import Graph, Matching
from rounding_schemes import GreedyRoundingScheme, SimpleRecursiveRoundingScheme, SimulatedRecursiveRoundingScheme
import multiprocessing as mp
import pickle
import copy
import random


class Evaluator:
    def __init__(self, fractional_matching, edge_arrival_order, num_rounds):
        self.graph = Graph(edge_arrival_order)

        # self.graph.draw()

        self.graph.set_fractional_matching(fractional_matching)
        self.num_rounds = num_rounds
        self.matched_count = {edge: 0 for edge in self.graph.graph.edges()}

    def set_rounding_scheme(self, rounding_scheme):
        self.rounding_scheme = rounding_scheme

    # def initialize_experiment(self):
    #     self.graph.time = 0
    #     self.graph.revealed_edges = []
    #     self.rounding_scheme.matching = Matching(self.graph)
    #     self.rounding_scheme.initialize()

    @staticmethod
    def execute_round(rounding_scheme_instance):
        matched_edges, estimated_unmatched_probabilities = rounding_scheme_instance.execute(debug=True)

        result = {
            "matched_edges": matched_edges,
            "estimated_unmatched_probabilities": estimated_unmatched_probabilities
        }
        # print(f"Round completed.")

        return result
    

    def experiment(self, parallel=True):
        if parallel:
            print(f"Running {self.num_rounds} rounds in parallel using {mp.cpu_count()} CPU cores...")
            rounding_scheme_instances = [copy.deepcopy(self.rounding_scheme) for _ in range(self.num_rounds)]
            
            print(f"Starting parallel execution...")
            with mp.Pool(processes=mp.cpu_count()) as pool:
                results = pool.map(Evaluator.execute_round, rounding_scheme_instances)

            print(f"Parallel execution completed. Processing results...")
            for i, result in enumerate(results):
                matched_edges = result["matched_edges"]
                estimated_unmatched_probabilities = result["estimated_unmatched_probabilities"]
                # print(f"Round {i}: Matched edge {result['matched_edges']}")

                with open("estimated_probabilities20.csv", "a") as f:
                    f.write(f"{len(self.graph.revealed_edges)},")
                    for edge in self.graph.edge_arrival_order:
                        prob = estimated_unmatched_probabilities.get(edge, 0)
                        f.write(f"{prob},")
                    f.write("\n")

                for edge in matched_edges:
                    u, v = edge
                    if edge in self.matched_count:
                        self.matched_count[edge] += 1
                    elif (v, u) in self.matched_count:
                        self.matched_count[(v, u)] += 1
                    else:
                        print(f"Warning: Matched edge {edge} not found in matched_count dictionary.")
        else:
            for i in range(self.num_rounds):
                result = self.execute_round()
                print(f"Round {i}: Matched edge {result['matched_edges']}")

        matching_probabilities = {edge: count / self.num_rounds for edge, count in self.matched_count.items()}

        """ 
        The minimum value of this matching probability across all edges should be at least c times the weight of the edge in the fractional matching.
        """
        scaled_matching_probabilities = {edge: prob / self.graph.get_edge_weight(edge[0], edge[1]) for edge, prob in matching_probabilities.items()}

        return scaled_matching_probabilities

if __name__ == "__main__":
    # fractional_matching = { (0, 1): 0.5, (1, 2): 0.5, (0, 2): 0.5 }
    # edge_arrival_order = [(0, 1), (1, 2), (0, 2)]

    # # Example with a star graph with uniform fractional matching, |V|=20
    # fractional_matching = { (0, i): 1/100 for i in range(1, 101) }
    # edge_arrival_order = [(0, i) for i in range(1, 101)]

    # # Complete graph with uniform fractional matching, |V|=6
    # fractional_matching = { (i, j): 0.2 for i in range(6) for j in range(i+1, 6) }
    # edge_arrival_order = [(i, j) for i in range(6) for j in range(i+1, 6)]


    # # Example with a complete graph with uniform fractional matching, |V|=20
    # fractional_matching = { (i, j): 1/19 for i in range(20) for j in range(i+1, 20) }
    # edge_arrival_order = [(i, j) for i in range(20) for j in range(i+1, 20)]

    # Bipartite graph with uniform fractional matching, |V|=10 on each side
    fractional_matching = { (i, j): 1/20 for i in range(20) for j in range(20, 40) }

    # shuffle edge arrival order
    edge_arrival_order = [(i, j) for i in range(20) for j in range(20, 40)]
    random.shuffle(edge_arrival_order)

    c_guarantee = 3/4

    evaluator = Evaluator(fractional_matching, edge_arrival_order, num_rounds=20000)
    # evaluator.set_rounding_scheme(GreedyRoundingScheme(evaluator.graph))
    # evaluator.set_rounding_scheme(SimpleRecursiveRoundingScheme(evaluator.graph, c=c_guarantee))
    evaluator.set_rounding_scheme(SimulatedRecursiveRoundingScheme(evaluator.graph, c=c_guarantee, num_sim_instances=10000))

    with open("estimated_probabilities20.csv", "w") as f:
        f.write("Round,")
        for edge in edge_arrival_order:
            f.write(f'"{edge}",')
        f.write("\n")

    scaled_probabilities = evaluator.experiment()

    print(scaled_probabilities)
    print("Worst-case probabilities:", min(scaled_probabilities.values()))
    