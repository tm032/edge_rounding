import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ESTIMATED_PROBABILITIES_DIR = "estimated_unmatched_probabilities/"
SUMMARY_RESULTS_DIR = "summary_results/"
FIGURES_DIR = "figures/"

def analyze_variance(file_name):
    df = pd.read_csv(f"{ESTIMATED_PROBABILITIES_DIR}{file_name}")
    variance_results = {}
    for edge in df.columns:
        variance_results[edge] = {
            "mean": df[edge].mean(),
            "std": df[edge].std(),
            "variance": df[edge].var()
        }
    return variance_results

def plot_mean_and_std(variance_results):
    edges = list(variance_results.keys())
    means = [variance_results[edge]["mean"] for edge in edges]
    stds = [variance_results[edge]["std"] for edge in edges]
    variance = [variance_results[edge]["variance"] for edge in edges]

    plt.figure(figsize=(10, 6))
    
    # Calculate 95% confidence intervals
    ci = 1.96 * np.array(stds) / np.sqrt(len(edges))
    upper_ci = np.array(means) + ci
    lower_ci = np.array(means) - ci
    
    # Plot mean and confidence intervals
    plt.errorbar(edges, means, yerr=ci, fmt='o', ecolor='r', capsize=5, label='Mean with 95% CI')
    # plt.scatter(edges, means, label='Mean', color='blue')

    # Do not show x-axis labels to avoid clutter
    plt.xticks([])
    
        # Add error bars to represent the confidence intervals
    
    plt.xlabel("Edges (arriving from left to right)")
    plt.ylabel(f"Estimated unmatched probability")
    # plt.title(f"Estimated unmatched probabilities for non-uniform bipartite graph with {n} vertices, c=0.8, r=0.8")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}variance_analysis_{n}.png")
    plt.show()

if __name__ == "__main__":
    n = 10
    file_name = f"nonuniform_bipartite_{n}_{n}_order_0_mc_c80_r80_sim10000.csv"
    variance_results = analyze_variance(file_name)
    plot_mean_and_std(variance_results)