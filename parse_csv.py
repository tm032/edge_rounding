import pandas as pd

df = pd.read_csv("estimated_probabilities20.csv")

# print statistics for each edge
for edge in df.columns[1:]:
    print(f"Edge {edge}:")
    print(f"  Mean estimated unmatched probability: {df[edge].mean()}")
    print(f"  Std deviation of estimated unmatched probability: {df[edge].std()}")