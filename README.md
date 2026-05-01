# Simulation-based Recursive Edge Rounding Scheme
Tsugunobu Miyake  

## Purpose
This is the source code used for the Course Project for Simulation Theory and Methodology class. It implements and evaluates the Simulation-based Recursive Edge Rounding Scheme for the Online Fractional Edge Rounding Problem.

## Directory and File Structures
- `graph.py`: Defines the graph's structures.
- `generate_graph_instances.py`: Generates graphs used in the experiments.
- `rounding_schemes.py`: Defines the Rounding Schemes
- `evaluate_schemes.py`: Evaluation pipeline for the Rounding Schemes.
- `main.py`: Executes the experiments.
- `raw_results/`: Stores the raw results of each simulated performance of the rounding scheme.
- `summary_results/`: Contains code that analyzes the raw output and the CSV file summarizing each experiment.
- `graph_instances/`: Contains the graph instances with edge weights and edge arrival order.
- `figures/`: Contains figures used in the final report and the presentation.
- `estimated_unmatched_probabilities/`: Contains raw data of $\Pr[\lnot M_u(e) \land \lnot M_v(e)]$ estimation for debug purposes.