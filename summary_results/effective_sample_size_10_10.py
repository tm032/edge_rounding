import pandas as pd
import matplotlib.pyplot as plt
import json
RAW_RESULTS_DIR = "raw_results/"
SUMMARY_RESULTS_DIR = "summary_results/"
FIGURES_DIR = "figures/"

def parse_json_files():
    with open(f"{SUMMARY_RESULTS_DIR}/effective_sample_size_results_bipartite_10_10.csv", "w") as f:
        f.write("rounding_scheme,r,c,effective_sample_size\n")
    for r in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        for c in [0.5, 0.6, 2/3, 0.7, 3/4, 0.8, 0.9, 1.0]:
            simulated_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_bipartite_10_10_order_0_mc_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
            simple_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_bipartite_10_10_order_0_si_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
            with open(f"{SUMMARY_RESULTS_DIR}/effective_sample_size_results_bipartite_10_10.csv", "a") as f:
                f.write(f"simulated,{r},{c},{simulated_scheme_data['effective_sample_size']}\n")
                f.write(f"simple,{r},{c},{simple_scheme_data['effective_sample_size']}\n")

def plot_effective_sample_size():
    markers = {
        0.0: "o",
        0.2: "s",
        0.4: "D",
        0.6: "^",
        0.8: "v",
        1.0: "P"
    }

    df = pd.read_csv(f"{SUMMARY_RESULTS_DIR}/effective_sample_size_results_bipartite_10_10.csv")
    fig, ax = plt.subplots(1,2, figsize=(10, 6))
    for r in sorted(df["r"].unique()):
        subset = df[df["rounding_scheme"] == "simulated"]
        ax[1].plot(subset[subset["r"] == r]["c"], subset[subset["r"] == r]["effective_sample_size"], label=f"$\\lambda={r}$", marker=markers.get(r, 'o'))
    ax[1].set_title("Bipartite Graph - Simulated Rounding Scheme")
    ax[1].set_xlabel("Target guarantee ($\\tilde{c}$)")
    ax[1].set_ylabel("Effective Sample Size")
    ax[1].legend()
    ax[1].grid(True)
    ax[1].minorticks_on()

    for r in sorted(df["r"].unique()):
        subset = df[df["rounding_scheme"] == "simple"]
        ax[0].plot(subset[subset["r"] == r]["c"], subset[subset["r"] == r]["effective_sample_size"], label=f"$\\lambda={r}$", marker=markers.get(r, 'o'))
    ax[0].set_title("Bipartite Graph - Trivial Rounding Scheme")
    ax[0].set_xlabel("Target guarantee ($\\tilde{c}$)")
    ax[0].set_ylabel("Effective Sample Size")
    ax[0].legend()
    ax[0].grid(True)
    ax[0].minorticks_on()
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/effective_sample_size_bipartite_10_10.png")
    plt.show()

if __name__ == "__main__":
    parse_json_files()
    plot_effective_sample_size()
