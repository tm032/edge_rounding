import numpy as np
import pandas as pd
import json 
import matplotlib.pyplot as plt

RAW_RESULTS_DIR = "raw_results/"
SUMMARY_RESULTS_DIR = "summary_results/"
FIGURES_DIR = "figures/"

def parse_json_files():
    with open(SUMMARY_RESULTS_DIR + "experiment_2_results.csv", "w") as f:
        f.write("graph,r,c,rounding_scheme,worst_case_guarantee\n")

    for r in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        for c in [0.5, 0.6, 2/3, 0.7, 3/4, 0.8, 0.9, 1.0]:
            # Star Graph
            simple_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_star_20_order_0_tr_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
            sim_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_star_20_order_0_mc_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
            # Process the data and write to summary file
            with open(SUMMARY_RESULTS_DIR + "experiment_2_results.csv", "a") as f:
                f.write(f"star,{r},{c},simple,{simple_scheme_data['min_scaled_matching_probability']}\n")
                f.write(f"star,{r},{c},simulated,{sim_scheme_data['min_scaled_matching_probability']}\n")

            # Tree Graph
            simple_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_tree_3_4_order_0_tr_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
            sim_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_tree_3_4_order_0_mc_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
            with open(SUMMARY_RESULTS_DIR + "experiment_2_results.csv", "a") as f:
                f.write(f"tree,{r},{c},simple,{simple_scheme_data['min_scaled_matching_probability']}\n")
                f.write(f"tree,{r},{c},simulated,{sim_scheme_data['min_scaled_matching_probability']}\n")

            # Complete Graph
            simple_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_complete_10_order_0_si_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
            sim_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_complete_10_order_0_mc_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
            with open(SUMMARY_RESULTS_DIR + "experiment_2_results.csv", "a") as f:
                f.write(f"complete,{r},{c},simple,{simple_scheme_data['min_scaled_matching_probability']}\n")
                f.write(f"complete,{r},{c},simulated,{sim_scheme_data['min_scaled_matching_probability']}\n")

            # Bipartite Graph
            simple_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_bipartite_10_10_order_0_si_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
            sim_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_bipartite_10_10_order_0_mc_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
            with open(SUMMARY_RESULTS_DIR + "experiment_2_results.csv", "a") as f:
                f.write(f"bipartite,{r},{c},simple,{simple_scheme_data['min_scaled_matching_probability']}\n")
                f.write(f"bipartite,{r},{c},simulated,{sim_scheme_data['min_scaled_matching_probability']}\n")


def plot_results(graph_type):
    df = pd.read_csv(SUMMARY_RESULTS_DIR + "experiment_2_results.csv")
    filtered_df = df[(df["graph"] == graph_type)]

    fig, ax = plt.subplots(1, 2, figsize=(10, 6))

    # Plot for simple scheme
    for r in sorted(filtered_df["r"].unique()):
        subset = filtered_df[(filtered_df["rounding_scheme"] == "simple") & (filtered_df["r"] == r)]
        ax[0].plot(subset["c"], subset["worst_case_guarantee"], label=f"$\\lambda={r}$", marker='o')
    ax[0].set_title(f"{graph_type.capitalize()} Graph - Trivial Rounding Scheme")
    ax[0].set_xlabel("Target guarantee ($\\tilde{c}$)")
    ax[0].set_ylabel("Estimated guarantee ($\\hat{c}$)")
    ax[0].set_ylim(0, 1.05)  # Set y-axis limits to [0, 1.05] to ensure all points are visible and prevent overlap with x-axis
    ax[0].minorticks_on()  # Enable minor ticks to improve readability of the plot
    ax[0].grid(True)
    ax[0].legend()
    
    # Plot for simulated scheme
    for r in sorted(filtered_df["r"].unique()):
        subset = filtered_df[(filtered_df["rounding_scheme"] == "simulated") & (filtered_df["r"] == r)]
        ax[1].plot(subset["c"], subset["worst_case_guarantee"], label=f"$\\lambda={r}$", marker='o')
    ax[1].set_title(f"{graph_type.capitalize()} Graph - Simulated Rounding Scheme")
    ax[1].set_xlabel("Target guarantee ($\\tilde{c}$)")
    ax[1].set_ylabel("Estimated guarantee ($\\hat{c}$)")
    ax[1].set_ylim(0, 1.05)  # Set y-axis limits to [0, 1.05] to ensure all points are visible and prevent overlap with x-axis
    ax[1].minorticks_on()  # Enable minor ticks to improve readability of the plot
    ax[1].grid(True)
    ax[1].legend()

    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/{graph_type}_experiment_2_results.png")
    plt.show() 


def plot_results_all():
    df = pd.read_csv(SUMMARY_RESULTS_DIR + "experiment_2_results.csv")
    fig, axes = plt.subplots(2, 4, figsize=(18, 10))
    graph_types = ["star", "tree", "complete", "bipartite"]

    marker_styles = {
        0.0: "o",
        0.2: "s",
        0.4: "D",
        0.6: "^",
        0.8: "v",
        1.0: "P"
    }
    
    for i, graph_type in enumerate(graph_types):
        #Simple scheme
        ax = axes[0, i]
        for r in sorted(df["r"].unique()):
            subset = df[(df["rounding_scheme"] == "simple") & (df["graph"] == graph_type) & (df["r"] == r)]
            ax.plot(subset["c"], subset["worst_case_guarantee"], label=f"$\\lambda={r}$", marker=marker_styles.get(r, 'o'))
        ax.set_title(f"{graph_type.capitalize()} Graph - Trivial")
        ax.set_xlabel("Target guarantee ($\\tilde{c}$)")
        ax.set_ylabel("Estimated guarantee ($\\hat{c}$)")
        ax.set_ylim(0, 1.05)  # Set y-axis limits to
        ax.minorticks_on()  # Enable minor ticks to improve readability of the plot
        ax.grid(True)

        # Tiny legend size to prevent overlap with data points
        ax.legend(fontsize='small')

        # Simulated scheme
        ax = axes[1, i]
        for r in sorted(df["r"].unique()):
            subset = df[(df["rounding_scheme"] == "simulated") & (df["graph"] == graph_type) & (df["r"] == r)]
            ax.plot(subset["c"], subset["worst_case_guarantee"], label=f"$\\lambda={r}$", marker=marker_styles.get(r, 'o'))
        ax.set_title(f"{graph_type.capitalize()} Graph - Simulation-based")
        ax.set_xlabel("Target guarantee ($\\tilde{c}$)")
        ax.set_ylabel("Estimated guarantee ($\\hat{c}$)")
        ax.set_ylim(0, 1.05)  # Set y-axis limits to
        ax.minorticks_on()  # Enable minor ticks to improve readability of the plot
        ax.grid(True)


    # Smaller margin than plt.tight_layout() to fit all subplots nicely
    plt.subplots_adjust(wspace=0.3, hspace=0.4)

    plt.savefig(f"{FIGURES_DIR}/experiment_2_results_all.png")
    plt.show()


if __name__ == "__main__":
    # parse_json_files()
    # plot_results("complete")
    plot_results_all()