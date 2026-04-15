import matplotlib.pyplot as plt
import pandas as pd

result = pd.read_csv("summary_results/uniform_complete_bipartite_20.csv")

plt.figure(figsize=(10, 6))

# x axis: c
# y axis: scaled matching probability
# label |V| and scheme differentiation by color and marker

plt.xlabel("c")
plt.ylabel("Worst Case Guarantee")
plt.title("Worst Case Guarantee vs c for Different Schemes and Graph Sizes")
for scheme in result['rounding_scheme'].unique():
    for size in result['|V|'].unique():
        subset = result[(result['rounding_scheme'] == scheme) & (result['|V|'] == size)]
        plt.plot(subset['c'], subset['worst_case_guarantee'], marker='o', label=f"{scheme}, |V|={size}")
plt.legend()
plt.grid()
# plt.savefig("scaled_matching_probability_vs_c.png")
plt.show()
