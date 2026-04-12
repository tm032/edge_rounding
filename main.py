from evaluate_schemes import run_experiments
from rounding_schemes import SimulatedRecursiveRoundingSchemeWithIS, SimulatedRecursiveRoundingScheme, SimpleRecursiveRoundingScheme

# For selecting which rounding scheme to execute.
from rounding_schemes import SIMULATED_ROUNDING_SCHEME_WITH_IS, SIMULATED_ROUNDING_SCHEME, SIMPLE_ROUNDING_SCHEME

if __name__ == "__main__":
    simulation_parameters = {
        "graph_file": "unbalanced_star_10.json",
        "c_guarantee": 0.75,
        "experiment_name": "unbalanced_star_10_is_r00",
        "rounding_scheme_class": SIMULATED_ROUNDING_SCHEME_WITH_IS,
        "average_edge_weight": 1/9,
        "r": 0,
        "num_sim_instances": 10000,
        "parallel": True
    }

    result = run_experiments(simulation_parameters)



