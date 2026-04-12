import json

from graph import Graph, Matching
from rounding_schemes import GreedyRoundingScheme, SimpleRecursiveRoundingScheme, SimulatedRecursiveRoundingScheme, SimulatedRecursiveRoundingSchemeWithIS
import multiprocessing as mp
import pickle
import copy
import random


class Evaluator:
    def __init__(self, fractional_matching, edge_arrival_order, num_rounds, file_name="results.csv"):
        self.graph = Graph(edge_arrival_order)

        # self.graph.draw()
        self.file_name = file_name

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
        return rounding_scheme_instance.execute()
    

    def experiment(self, parallel=True):
        if parallel:
            print(f"Running {self.num_rounds} rounds in parallel using {mp.cpu_count()} CPU cores...")
            rounding_scheme_instances = [copy.deepcopy(self.rounding_scheme) for _ in range(self.num_rounds)]
            
            print(f"Starting parallel execution...")
            with mp.Pool(processes=mp.cpu_count()) as pool:
                results = pool.map(Evaluator.execute_round, rounding_scheme_instances)

            print(f"Parallel execution completed. Processing results...")

            if isinstance(self.rounding_scheme, SimulatedRecursiveRoundingScheme):
                for i, result in enumerate(results):
                    matched_edges = result["matched_edges"]
                    estimated_unmatched_probabilities = result["estimated_unmatched_probabilities"]

                    with open(self.file_name, "a") as f:
                        f.write(f"{len(self.graph.revealed_edges)},")
                        for edge in self.graph.edge_arrival_order:
                            prob = estimated_unmatched_probabilities.get(edge, 0)
                            f.write(f"{prob},")
                        f.write("\n")

                    if isinstance(self.rounding_scheme, SimulatedRecursiveRoundingSchemeWithIS):
                        simulation_weight = result["simulation_weight"]
                        for edge in matched_edges:
                            u, v = edge
                            if edge in self.matched_count:
                                self.matched_count[edge] += simulation_weight
                            elif (v, u) in self.matched_count:
                                self.matched_count[(v, u)] += simulation_weight
                            else:
                                print(f"Warning: Matched edge {edge} not found in matched_count dictionary.")
                    else:
                        for edge in matched_edges:
                            u, v = edge
                            if edge in self.matched_count:
                                self.matched_count[edge] += 1
                            elif (v, u) in self.matched_count:
                                self.matched_count[(v, u)] += 1
                            else:
                                print(f"Warning: Matched edge {edge} not found in matched_count dictionary.")
            else:
                for i, result in enumerate(results):
                    matched_edges = result["matched_edges"]

                    if isinstance(self.rounding_scheme, SimulatedRecursiveRoundingSchemeWithIS):
                        simulation_weight = result["simulation_weight"]
                        print(f"simulation weight: {simulation_weight}")
                        
                        for edge in matched_edges:
                            u, v = edge
                            if edge in self.matched_count:
                                self.matched_count[edge] += simulation_weight
                            elif (v, u) in self.matched_count:
                                self.matched_count[(v, u)] += simulation_weight
                            else:
                                print(f"Warning: Matched edge {edge} not found in matched_count dictionary.")
                    else:
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
                rounding_scheme_instance = copy.deepcopy(self.rounding_scheme)
                result = self.execute_round(rounding_scheme_instance)
                print(f"Round {i}: Matched edge {result['matched_edges']}")
                
                if isinstance(self.rounding_scheme, SimulatedRecursiveRoundingScheme):
                    estimated_unmatched_probabilities = result["estimated_unmatched_probabilities"]

                    with open(self.file_name, "a") as f:
                        f.write(f"{len(self.graph.revealed_edges)},")
                        for edge in self.graph.edge_arrival_order:
                            prob = estimated_unmatched_probabilities.get(edge, 0)
                            f.write(f"{prob},")
                        f.write("\n")

                if isinstance(self.rounding_scheme, SimulatedRecursiveRoundingSchemeWithIS):
                    simulation_weight = result["simulation_weight"]
                    # print(f"simulation weight: {simulation_weight}")
                    
                    for edge in result['matched_edges']:
                        u, v = edge
                        if edge in self.matched_count:
                            self.matched_count[edge] += 1
                        elif (v, u) in self.matched_count:
                            self.matched_count[(v, u)] += 1
                        else:
                            print(f"Warning: Matched edge {edge} not found in matched_count dictionary.")
                else:
                    for edge in result['matched_edges']:
                        u, v = edge
                        if edge in self.matched_count:
                            self.matched_count[edge] += 1
                        elif (v, u) in self.matched_count:
                            self.matched_count[(v, u)] += 1
                        else:
                            print(f"Warning: Matched edge {edge} not found in matched_count dictionary.")

        matching_probabilities = {edge: count / self.num_rounds for edge, count in self.matched_count.items()}

        print(matching_probabilities)

        """ 
        The minimum value of this matching probability across all edges should be at least c times the weight of the edge in the fractional matching.
        """
        scaled_matching_probabilities = {edge: prob / self.graph.get_edge_weight(edge[0], edge[1]) for edge, prob in matching_probabilities.items()}

        return scaled_matching_probabilities

if __name__ == "__main__":
    random.seed(42)
    # fractional_matching = { (0, 1): 0.5, (1, 2): 0.5, (0, 2): 0.5 }
    # edge_arrival_order = [(0, 1), (1, 2), (0, 2)]

    # Example with a star graph with uniform fractional matching, |V|=20
    fractional_matching = { (0, i): 0.005 for i in range(1, 21) }
    fractional_matching[0,17] = 0.91
    edge_arrival_order = [(0, i) for i in range(1, 21)]

    # # Complete graph with uniform fractional matching, |V|=6
    # fractional_matching = { (i, j): 0.2 for i in range(6) for j in range(i+1, 6) }
    # edge_arrival_order = [(i, j) for i in range(6) for j in range(i+1, 6)]


    # # Example with a complete graph with uniform fractional matching, |V|=20
    # fractional_matching = { (i, j): 1/19 for i in range(20) for j in range(i+1, 20) }
    # edge_arrival_order = [(i, j) for i in range(20) for j in range(i+1, 20)]

    # Bipartite graph with uniform fractional matching, |V|=10 on each side
    fractional_matching = { (i, j): 1/10 for i in range(10) for j in range(10, 20) }

    # shuffle edge arrival order
    edge_arrival_order = [(i, j) for i in range(10) for j in range(10, 20)]
    random.shuffle(edge_arrival_order)

    # # Bipartite graph with uniform fractional matching, |V|=15 on each side
    # fractional_matching = { (i, j): 1/10 for i in range(10) for j in range(10, 20) }

    # # shuffle edge arrival order
    # edge_arrival_order = [(i, j) for i in range(10) for j in range(10, 20)]
    # random.shuffle(edge_arrival_order)

    c_guarantee = 2/3
    experiment_name = "is_star_20"

    json_file_name = f"raw_results/{experiment_name}.json"
    csv_file_name = f"raw_results/{experiment_name}.csv"

    evaluator = Evaluator(fractional_matching, edge_arrival_order, num_rounds=10000, file_name=csv_file_name)
    # evaluator.set_rounding_scheme(GreedyRoundingScheme(evaluator.graph))
    # evaluator.set_rounding_scheme(SimpleRecursiveRoundingScheme(evaluator.graph, c=c_guarantee))
    # evaluator.set_rounding_scheme(SimulatedRecursiveRoundingScheme(evaluator.graph, c=c_guarantee, num_sim_instances=1000))

    evaluator.set_rounding_scheme(SimulatedRecursiveRoundingSchemeWithIS(evaluator.graph, average_edge_weight=0.05, c=c_guarantee, num_sim_instances=1000))


    # with open(evaluator.file_name, "w") as f:
    #     f.write("Round,")
    #     for edge in edge_arrival_order:
    #         f.write(f'"{edge}",')
    #     f.write("\n")

    scaled_probabilities = evaluator.experiment(parallel=True)

    print(scaled_probabilities)
    serializable_data = {str(k): v for k, v in scaled_probabilities.items()}
    json.dump(serializable_data, open(f"{json_file_name}", "w"), indent=4)
    print("Worst-case probabilities:", min(scaled_probabilities.values()))
    