import numpy as np
import pandas as pd
import json 
import matplotlib.pyplot as plt

RAW_RESULTS_DIR = "raw_results/"
SUMMARY_RESULTS_DIR = "summary_results/"
FIGURES_DIR = "figures/"

def parse_json_file():
    with open(SUMMARY_RESULTS_DIR + "experiment_2a_results.csv", "w") as f:
        f.write("r,c,rounding_scheme,worst_case_guarantee\n")

    for r in [0.8, 0.85, 0.9, 0.95, 1.0]:
        for c in [0.5, 0.6, 2/3, 0.7, 3/4, 0.8, 0.9, 1.0]:
            simple_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_complete_10_order_0_si_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
            sim_is_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_complete_10_order_0_mc_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))
            sim_scheme_data = json.load(open(f"{RAW_RESULTS_DIR}/nonuniform_complete_10_order_0_mc_c{int(c*100)}_r{int(r*100)}_sim10000.json", "r"))

            with open(RAW_RESULTS_DIR + "experiment_2a_results.csv", "a") as f:
                f.write(f"{r},{c},simple,{simple_scheme_data['min_scaled_matching_probability']}\n")
                f.write(f"{r},{c},simulated_is,{sim_is_scheme_data['min_scaled_matching_probability']}\n")
                f.write(f"{r},{c},simulated,{sim_scheme_data['min_scaled_matching_probability']}\n")


def plot_results():
    data = pd.read_csv(SUMMARY_RESULTS_DIR + "experiment_2a_results.csv")
    # Plotting
    fig, ax = plt.subplots(2,2, figsize=(10, 6))

    # Plot for simple scheme
    for r in sorted(data['r'].unique()):
        subset = data[(data['rounding_scheme'] == 'simple') & (data['r'] == r)]
        ax[0,0].plot(subset['c'], subset['worst_case_guarantee'], label=f"r={r}")
    ax[0,0].set_title("Simple Rounding Scheme")
    ax[0,0].set_xlabel("c")
    ax[0,0].set_ylabel("Worst-case Guarantee")
    ax[0,0].legend()

    # Plot for simulated scheme with IS
    for r in sorted(data['r'].unique()):
        subset = data[(data['rounding_scheme'] == 'simulated_is') & (data['r'] == r)]
        ax[0,1].plot(subset['c'], subset['worst_case_guarantee'], label=f"r={r}")
    ax[0,1].set_title("Simulated Rounding Scheme with IS")
    ax[0,1].set_xlabel("c")
    ax[0,1].set_ylabel("Worst-case Guarantee")
    ax[0,1].legend()

    # Plot for simulated scheme without IS
    for r in sorted(data['r'].unique()):
        subset = data[(data['rounding_scheme'] == 'simulated') & (data['r'] == r)]
        ax[1,0].plot(subset['c'], subset['worst_case_guarantee'], label=f"r={r}")
    ax[1,0].set_title("Simulated Rounding Scheme without IS")
    ax[1,0].set_xlabel("c")
    ax[1,0].set_ylabel("Worst-case Guarantee")
    ax[1,0].legend()


    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parse_json_file()
    #plot_results()