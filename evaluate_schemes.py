import json

from graph import Graph, GRAPH_INSTANCE_DIR
from rounding_schemes import SimpleRecursiveRoundingScheme, SimulatedRecursiveRoundingScheme, SimulatedRecursiveRoundingSchemeWithIS
from rounding_schemes import SIMPLE_ROUNDING_SCHEME, SIMULATED_ROUNDING_SCHEME, SIMULATED_ROUNDING_SCHEME_WITH_IS, SIMPLE_ROUNDING_SCHEME_FOR_TREE
import multiprocessing as mp
import numpy as np
from numpy.random import default_rng, SeedSequence
import copy

seed = 42

RAW_RESULTS_DIR = "raw_results/"
UNMATCHED_PROBABILITIES_DIR = "estimated_unmatched_probabilities/"

class Evaluator:
    def __init__(self, graph, num_rounds, file_name="results.csv"):
        self.graph = graph

        # self.graph.draw()
        self.file_name = file_name
        self.num_rounds = num_rounds
        self.matched_count = {edge: 0 for edge in self.graph.graph.edges()}

    def set_rounding_scheme(self, rounding_scheme):
        self.rounding_scheme = rounding_scheme

    @staticmethod
    def execute_round(rounding_scheme_instance, rng):
        return rounding_scheme_instance.execute(rng)

    def experiment(self, parallel=True):
        seed_sequence = SeedSequence(seed)
        child_seeds = seed_sequence.spawn(self.num_rounds)
        rngs = [default_rng(s) for s in child_seeds]

        if parallel:
            rounding_scheme_instances = [copy.deepcopy(self.rounding_scheme) for _ in range(self.num_rounds)]
            with mp.Pool(processes=mp.cpu_count()//2) as pool:
                results = pool.starmap(Evaluator.execute_round, [(instance, rng) for rng, instance in zip(rngs, rounding_scheme_instances)])
        else:
            results = []
            for i in range(self.num_rounds):
                rounding_scheme_instance = copy.deepcopy(self.rounding_scheme)
                result = self.execute_round(rounding_scheme_instance, rngs[i])
                results.append(result)
        
        if isinstance(self.rounding_scheme, SimulatedRecursiveRoundingScheme):
            with open(self.file_name, "w") as f:
                    for edge in self.graph.edge_arrival_order:
                        f.write(f'"{edge}",')
                    f.write("\n")


        for result in results:
            if isinstance(self.rounding_scheme, SimulatedRecursiveRoundingScheme):
                estimated_unmatched_probabilities = result["estimated_unmatched_probabilities"]

                with open(self.file_name, "a") as f:
                    for edge in self.graph.edge_arrival_order:
                        u, v = edge
                        if edge in estimated_unmatched_probabilities:
                            prob = estimated_unmatched_probabilities[edge]
                        elif (v, u) in estimated_unmatched_probabilities:
                            prob = estimated_unmatched_probabilities[(v, u)]
                        else:
                            raise ValueError(f"Edge {edge} not found in estimated_unmatched_probabilities dictionary.")

                        f.write(f"{prob},")
                    f.write("\n")

            simulation_weight = result["simulation_weight"]                    
            for edge in result['matched_edges']:
                u, v = edge
                if edge in self.matched_count:
                    self.matched_count[edge] += simulation_weight
                elif (v, u) in self.matched_count:
                    self.matched_count[(v, u)] += simulation_weight
                else:
                    print(f"Warning: Matched edge {edge} not found in matched_count dictionary.")

        matching_counts = {edge: count for edge, count in self.matched_count.items()}

        matching_probabilities = {edge: count / self.num_rounds for edge, count in self.matched_count.items()}

        """ 
        The minimum value of this matching probability across all edges should be at least c times the weight of the edge in the fractional matching.
        """
        scaled_matching_probabilities = {edge: prob / self.graph.get_edge_weight(edge[0], edge[1]) for edge, prob in matching_probabilities.items()}

        result = {
            "min_scaled_matching_probability": min(scaled_matching_probabilities.values()),
            "scaled_matching_probabilities": scaled_matching_probabilities,
            "matching_probabilities": matching_probabilities,
            "matching_counts": matching_counts,
        }

        return result
    
def seriarize_results_for_json(results):
    serializable_results = {}
    for summary_key, summary_value in results.items():
        if isinstance(summary_value, dict):
            serializable_results[summary_key] = {str(k): v for k, v in summary_value.items()}
        else:
            try:
                float(summary_value) # Check if it's a number
                serializable_results[summary_key] = summary_value
            except (ValueError, TypeError):
                serializable_results[summary_key] = str(summary_value)

    return serializable_results
    
def run_experiments(parameters):
    graph_file = parameters["graph_file"]
    graph = Graph(json_file=graph_file)


    c_guarantee = parameters.get("c_guarantee", 0.75)
    experiment_name = parameters.get("experiment_name", "experiment")
    rounding_scheme_class = parameters.get("rounding_scheme_class", SimulatedRecursiveRoundingSchemeWithIS)
    parallel = parameters.get("parallel", True)

    raw_result_file_name = f"{RAW_RESULTS_DIR}/{experiment_name}.json"
    unmatched_prob_file_name = f"{UNMATCHED_PROBABILITIES_DIR}/{experiment_name}.csv"

    r = parameters.get("r", 0.7)
    average_edge_weight = parameters.get("average_edge_weight", 1 / graph.graph.number_of_edges())

    evaluator = Evaluator(graph, num_rounds=10000, file_name=unmatched_prob_file_name)

    if rounding_scheme_class == SIMULATED_ROUNDING_SCHEME_WITH_IS:
        num_sim_instances = parameters.get("num_sim_instances", 10000)
        evaluator.set_rounding_scheme(SimulatedRecursiveRoundingSchemeWithIS(graph, average_edge_weight=average_edge_weight, c=c_guarantee, num_sim_instances=num_sim_instances, r=r))
    elif rounding_scheme_class == SIMULATED_ROUNDING_SCHEME:
        num_sim_instances = parameters.get("num_sim_instances", 10000)
        evaluator.set_rounding_scheme(SimulatedRecursiveRoundingScheme(graph, average_edge_weight=average_edge_weight, c=c_guarantee, r=r, num_sim_instances=num_sim_instances))
    elif rounding_scheme_class == SIMPLE_ROUNDING_SCHEME:
        evaluator.set_rounding_scheme(SimpleRecursiveRoundingScheme(graph, average_edge_weight=average_edge_weight, c=c_guarantee, r=r, is_tree=False))
    elif rounding_scheme_class == SIMPLE_ROUNDING_SCHEME_FOR_TREE:
        evaluator.set_rounding_scheme(SimpleRecursiveRoundingScheme(graph, average_edge_weight=average_edge_weight, c=c_guarantee, r=r, is_tree=True))
    else:
        raise ValueError(f"Unsupported rounding scheme class: {rounding_scheme_class}")
    
    result = evaluator.experiment(parallel=parallel)
    result["simulation_parameters"] = parameters

    json_data = seriarize_results_for_json(result)  
    json.dump(json_data, open(f"{raw_result_file_name}", "w"), indent=4)

    print(f"Experiment '{experiment_name}' guarantee:", result["min_scaled_matching_probability"])
    return result
    