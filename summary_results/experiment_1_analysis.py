import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

RAW_RESULTS_DIR = "raw_results/"
UNMATCHED_PROBABILITIES_DIR = "estimated_unmatched_probabilities/"
SUMMARY_RESULTS_DIR = "summary_results/"
FIGURES_DIR = "figures/"

c = [0.5, 0.6, 2/3, 0.7, 3/4, 0.8, 0.9, 1.0]

def parse_json_file():
    with open(SUMMARY_RESULTS_DIR + "experiment_1_results.csv", "w") as f:
        f.write("graph,rounding_scheme,c,worst_case_guarantee\n")

    # Star graph
    for c_value in c:
        simple_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/uniform_star_20_order_0_tr_c{int(c_value*100)}_r100_sim10000.json", "r"))
        sim_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/uniform_star_20_order_0_mc_c{int(c_value*100)}_r100_sim10000.json", "r"))

        with open(SUMMARY_RESULTS_DIR + "experiment_1_results.csv", "a") as f:
            f.write(f"star,simple,{c_value},{simple_scheme_data['min_scaled_matching_probability']}\n")
            f.write(f"star,simulated,{c_value},{sim_scheme_data['min_scaled_matching_probability']}\n")

    # Tree graph
    for c_value in c:
        simple_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/uniform_tree_3_4_order_0_tr_c{int(c_value*100)}_r100_sim10000.json", "r"))
        sim_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/uniform_tree_3_4_order_0_mc_c{int(c_value*100)}_r100_sim10000.json", "r"))

        with open(SUMMARY_RESULTS_DIR + "experiment_1_results.csv", "a") as f:
            f.write(f"tree,simple,{c_value},{simple_scheme_data['min_scaled_matching_probability']}\n")
            f.write(f"tree,simulated,{c_value},{sim_scheme_data['min_scaled_matching_probability']}\n")

    # Complete graph
    for c_value in c:
        simple_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/uniform_complete_10_order_0_si_c{int(c_value*100)}_r100_sim10000.json", "r"))
        sim_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/uniform_complete_10_order_0_mc_c{int(c_value*100)}_r100_sim10000.json", "r"))

        with open(SUMMARY_RESULTS_DIR + "experiment_1_results.csv", "a") as f:
            f.write(f"complete,simple,{c_value},{simple_scheme_data['min_scaled_matching_probability']}\n")
            f.write(f"complete,simulated,{c_value},{sim_scheme_data['min_scaled_matching_probability']}\n")

    # Bipartite graph
    for c_value in c:
        simple_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/uniform_bipartite_10_10_order_0_si_c{int(c_value*100)}_r100_sim10000.json", "r"))
        sim_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/uniform_bipartite_10_10_order_0_mc_c{int(c_value*100)}_r100_sim10000.json", "r"))

        with open(SUMMARY_RESULTS_DIR + "experiment_1_results.csv", "a") as f:
            f.write(f"bipartite,simple,{c_value},{simple_scheme_data['min_scaled_matching_probability']}\n")
            f.write(f"bipartite,simulated,{c_value},{sim_scheme_data['min_scaled_matching_probability']}\n")

def plot_results():
    titles = {
        "star": "Star Graph (20 leaves)",
        "tree": "Tree Graph  (3-ary tree of height 4)",
        "complete": "Complete Graph (10 nodes)",
        "bipartite": "Bipartite Graph (10 left nodes, 10 right nodes)"
    }

    rounding_scheme_labels = {
        "simple": "Simple Rounding",
        "simulated": "Simulated Rounding (with Crude MC)"
    }

    df = pd.read_csv(SUMMARY_RESULTS_DIR + "experiment_1_results.csv")

    df.rounding_scheme = df.rounding_scheme.map(rounding_scheme_labels)
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    graph_types = df["graph"].unique()
    for i, graph_type in enumerate(graph_types):
        ax = axes[i//2, i%2]
        graph_df = df[df["graph"] == graph_type]
        for rounding_scheme in graph_df["rounding_scheme"].unique():
            scheme_df = graph_df[graph_df["rounding_scheme"] == rounding_scheme]
            ax.plot(scheme_df["c"], scheme_df["worst_case_guarantee"], marker='o', label=rounding_scheme)
            ax.margins(y=0.1)  # Add some vertical margin to prevent overlap of points with x-axis

        ax.set_title(f"{titles.get(graph_type, graph_type.capitalize())}")
        ax.set_xlabel("c")
        ax.set_ylabel("Worst-case Guarantee")
        ax.legend()
        ax.grid(True)

    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/experiment_1_results.png")
    plt.show()


if __name__ == "__main__":
    # parse_json_file()
    plot_results()


        