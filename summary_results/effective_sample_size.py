import pandas as pd
import matplotlib.pyplot as plt
import json
RAW_RESULTS_DIR = "raw_results/"
SUMMARY_RESULTS_DIR = "summary_results/"
FIGURES_DIR = "figures/"


def parse_json_files():
    with open(f"{SUMMARY_RESULTS_DIR}/effective_sample_size_results_bipartite.csv", "w") as f:
        f.write("n_vertices,rounding_scheme,r,c,effective_sample_size\n")
    r=0.8
    
    for n_vertices in [10, 20, 30]:
        for c in [0.5, 0.6, 2/3, 0.7, 3/4, 0.8, 0.9, 1.0]:
            nonuniform_simulated_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_bipartite_{n_vertices}_{n_vertices}_order_0_mc_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))

            with open(f"{SUMMARY_RESULTS_DIR}/effective_sample_size_results_bipartite.csv", "a") as f:
                f.write(f"{n_vertices},simulated,{r},{c},{nonuniform_simulated_scheme_data['effective_sample_size']}\n")

def plot_effective_sample_size():
    markers = {
        10: "o",
        20: "s",
        30: "D"
    }

    df = pd.read_csv(f"{SUMMARY_RESULTS_DIR}/effective_sample_size_results_bipartite.csv")
    plt.figure(figsize=(8, 5))
    for n_vertices in sorted(df["n_vertices"].unique()):
        subset = df[df["n_vertices"] == n_vertices]
        plt.plot(subset[subset["rounding_scheme"] == "simulated"]["c"], subset[subset["rounding_scheme"] == "simulated"]["effective_sample_size"], label=f"|U|=|V|={n_vertices}", marker=markers.get(n_vertices, 'o'))
    # plt.title("Effective Sample Size for Simulated Rounding Scheme with different graph sizes")
    plt.xlabel("Target guarantee ($\\tilde{c}$)")
    plt.ylabel("Effective Sample Size")
    plt.ylim(0, 10000)  # Set y-axis limit to the total number of simulations to better visualize differences in effective sample size
    plt.grid(True)
    plt.minorticks_on()  # Enable minor ticks to improve readability of the plot
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/effective_sample_size_bipartite.png")
    plt.show()
    

if __name__ == "__main__":
    # parse_json_files()
    plot_effective_sample_size()
