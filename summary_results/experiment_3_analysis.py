import pandas as pd
import json
import matplotlib.pyplot as plt

RAW_RESULTS_DIR = "raw_results/"
SUMMARY_RESULTS_DIR = "summary_results/"
FIGURES_DIR = "figures/"

def parse_json_files():
    with open(SUMMARY_RESULTS_DIR + "experiment_3_results.csv", "w") as f:
        f.write("weights,order,c,rounding_scheme,worst_case_guarantee\n")
    
    for order in [0, 1, 2, 3, 4]:
        for c in [0.5, 0.6, 2/3, 0.7, 3/4, 0.8, 0.9, 1.0]:
            for weights in ["uniform", "nonuniform"]:
                r = 1 if weights == "uniform" and order == 0 else 0.8

                # Bipartite Graph
                if weights == "uniform":
                    simple_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/uniform_bipartite_10_10_order_{order}_si_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
                    sim_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/uniform_bipartite_10_10_order_{order}_mc_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))

                else:
                    simple_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_bipartite_10_10_order_{order}_si_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
                    sim_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_bipartite_10_10_order_{order}_mc_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
                
                with open(SUMMARY_RESULTS_DIR + "experiment_3_results.csv", "a") as f:
                    f.write(f"{weights},{order},{c},simple,{simple_scheme_data['min_scaled_matching_probability']}\n")
                    f.write(f"{weights},{order},{c},simulated,{sim_scheme_data['min_scaled_matching_probability']}\n")

def plot_results():
    df = pd.read_csv(SUMMARY_RESULTS_DIR + "experiment_3_results.csv")

    fig, ax = plt.subplots(2, 2, figsize=(10, 8))
    
    marker_styles = {
        0: "o",
        1: "s",
        2: "D",
        3: "^",
        4: "v"
    }

    for i, weights in enumerate(["uniform", "nonuniform"]):
        for j, rounding_scheme in enumerate(["simple", "simulated"]):
            subset = df[(df["weights"] == weights) & (df["rounding_scheme"] == rounding_scheme)]
            for order in sorted(subset["order"].unique()):
                order_subset = subset[subset["order"] == order]
                ax[i][j].plot(order_subset["c"], order_subset["worst_case_guarantee"], label=f"order={order}", marker=marker_styles.get(order, 'o'))
            ax[i][j].set_title(f"{weights.capitalize()} Weights - " + ("Trivial Rounding Scheme" if rounding_scheme == "simple" else "Simulation-based Rounding Scheme"))
            ax[i][j].set_xlabel("Target guarantee ($\\tilde{c}$)")
            ax[i][j].set_ylabel("Estimated guarantee ($\\hat{c}$)")
            ax[i][j].legend()
            ax[i][j].minorticks_on()
            ax[i][j].grid(True)
            ax[i][j].set_ylim(0, 1.05)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR + "experiment_3_results.png")
    plt.show()

if __name__ == "__main__":
    # parse_json_files()
    plot_results()
            