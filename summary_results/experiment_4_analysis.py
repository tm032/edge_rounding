import pandas as pd
import matplotlib.pyplot as plt
import json

RAW_DATA_DIR = "raw_results/"
SUMMARY_DATA_DIR = "summary_results/"

def parse_json_files():
    with open(SUMMARY_DATA_DIR + "experiment_4_results.csv", "w") as f:
        f.write("weights,num_vertices,rounding_scheme,c,worst_case_guarantee\n")

    for weights in ["uniform", "nonuniform"]:
        for num_vertices in [10, 20, 30]:
            r = 1 if weights == "uniform" and num_vertices == 10 else 0.8

            for c in [0.5, 0.6, 2/3, 0.7, 3/4, 0.8, 0.9, 1.0]:
                if weights == "uniform":
                    sim_scheme_data = json.load(open(f"{RAW_DATA_DIR}/uniform_bipartite_{num_vertices}_{num_vertices}_order_0_mc_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
                    with open(SUMMARY_DATA_DIR + "experiment_4_results.csv", "a") as f:
                        f.write(f"{weights},{num_vertices},simulated,{c},{sim_scheme_data['min_scaled_matching_probability']}\n")
                else:
                    sim_scheme_data = json.load(open(f"{RAW_DATA_DIR}/nonuniform_bipartite_{num_vertices}_{num_vertices}_order_0_mc_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
                    with open(SUMMARY_DATA_DIR + "experiment_4_results.csv", "a") as f:
                        f.write(f"{weights},{num_vertices},simulated,{c},{sim_scheme_data['min_scaled_matching_probability']}\n")

def plot_results():
    df = pd.read_csv(SUMMARY_DATA_DIR + "experiment_4_results.csv")

    fig, ax = plt.subplots(1, 2, figsize=(10, 6))
    marker_styles = {
        10: "o",
        20: "s",
        30: "D"
    }

    for i, weights in enumerate(["uniform", "nonuniform"]):
        subset = df[df["weights"] == weights]
        for num_vertices in sorted(subset["num_vertices"].unique()):
            num_vertices_subset = subset[subset["num_vertices"] == num_vertices]
            ax[i].plot(num_vertices_subset["c"], num_vertices_subset["worst_case_guarantee"], label=f"|U|=|V|={num_vertices}", marker=marker_styles.get(num_vertices, 'o'))
        ax[i].set_title(f"{weights.capitalize()} Weights")
        ax[i].set_xlabel("Target guarantee ($\\tilde{c}$)")
        ax[i].set_ylabel("Estimated guarantee ($\\hat{c}$)")
        ax[i].legend()
        ax[i].grid(True)
        ax[i].minorticks_on()
        ax[i].set_ylim(0, 1.05)
    
    plt.tight_layout()
    plt.savefig("figures/experiment_4_results.png")
    plt.show()

    
if __name__ == "__main__":
    # parse_json_files()
    plot_results()