import json
import random

from graph import BipartiteGraph, CompleteGraph, StarGraph, TreeGraph, GRAPH_INSTANCE_DIR

if __name__ == "__main__":
    balanced_bipartite_graph = BipartiteGraph(num_left_vertices=10, num_right_vertices=10)
    balanced_bipartite_graph.set_uniform_edge_weights(1/10)
    balanced_bipartite_graph.randomize_edge_arrival_order(seed=42)
    balanced_bipartite_graph.export_to_json("balanced_bipartite_10_10.json")

    unbalanced_bipartite_graph = BipartiteGraph(num_left_vertices=10, num_right_vertices=10)
    unbalanced_bipartite_graph.set_unbalanced_edge_weights(0.5, 0.5, seed=42)
    unbalanced_bipartite_graph.randomize_edge_arrival_order(seed=42)
    unbalanced_bipartite_graph.export_to_json("unbalanced_bipartite_10_10.json")

    balanced_tree_graph = TreeGraph(r=3, h=4)
    balanced_tree_graph.set_uniform_edge_weights(1/4)
    balanced_tree_graph.randomize_edge_arrival_order(seed=42)
    balanced_tree_graph.export_to_json("balanced_tree_3_4.json")

    unbalanced_tree_graph = TreeGraph(r=3, h=4)
    unbalanced_tree_graph.set_unbalanced_edge_weights(0.5, 0.5, seed=42)
    unbalanced_tree_graph.randomize_edge_arrival_order(seed=42)
    unbalanced_tree_graph.export_to_json("unbalanced_tree_3_4.json")

    balanced_star_graph = StarGraph(num_leaves=10)
    balanced_star_graph.set_uniform_edge_weights(1/10)
    balanced_star_graph.randomize_edge_arrival_order(seed=42)
    balanced_star_graph.export_to_json("balanced_star_10.json")

    unbalanced_star_graph = StarGraph(num_leaves=10)
    unbalanced_star_graph.set_unbalanced_edge_weights(0.5, 0.5, seed=42)
    unbalanced_star_graph.randomize_edge_arrival_order(seed=42)
    unbalanced_star_graph.export_to_json("unbalanced_star_10.json")

    balanced_complete_graph = CompleteGraph(num_vertices=10)
    balanced_complete_graph.set_uniform_edge_weights(1/9)
    balanced_complete_graph.randomize_edge_arrival_order(seed=42)
    balanced_complete_graph.export_to_json("balanced_complete_10.json")

    unbalanced_complete_graph = CompleteGraph(num_vertices=10)
    unbalanced_complete_graph.set_unbalanced_edge_weights(0.5, 0.5, seed=42)
    unbalanced_complete_graph.randomize_edge_arrival_order(seed=42)
    unbalanced_complete_graph.export_to_json("unbalanced_complete_10.json")


# graph_instance_dir = "graph_instances/"
# seed = 42

# random.seed(seed)

# def save_graph_instance(fractional_matching, edge_arrival_order, file_name):
#     with open(graph_instance_dir + file_name, "w") as f:
#         json.dump({
#             "fractional_matching": {str(k): v for k, v in fractional_matching.items()},
#             "edge_arrival_order": edge_arrival_order
#         }, f, indent=4)

# def parse_graph_instance(file_name):
#     with open(graph_instance_dir + file_name, "r") as f:
#         data = json.load(f)
#         fractional_matching = {eval(k): v for k, v in data["fractional_matching"].items()}
#         edge_arrival_order = [eval(edge) for edge in data["edge_arrival_order"]]
#         return fractional_matching, edge_arrival_order
    

# def star_graph_instance(num_leaves, fractional_weight):
#     fractional_matching = { (0, i): fractional_weight for i in range(1, num_leaves+1) }
#     edge_arrival_order = [(0, i) for i in range(1, num_leaves+1)]
#     return fractional_matching, edge_arrival_order

# def complete_graph_instance(num_vertices, fractional_weight, randomize_arrival=False):
#     fractional_matching = { (i, j): fractional_weight for i in range(num_vertices) for j in range(i+1, num_vertices) }
#     edge_arrival_order = [(i, j) for i in range(num_vertices) for j in range(i+1, num_vertices)]

#     if randomize_arrival:
#         random.shuffle(edge_arrival_order)

#     return fractional_matching, edge_arrival_order

# def bipartite_graph_instance(num_left_vertices, num_right_vertices, fractional_weight, randomize_arrival=False):
#     fractional_matching = { (i, j): fractional_weight for i in range(num_left_vertices) for j in range(num_left_vertices, num_left_vertices + num_right_vertices) }
#     edge_arrival_order = [(i, j) for i in range(num_left_vertices) for j in range(num_left_vertices, num_left_vertices + num_right_vertices)]

#     if randomize_arrival:
#         random.shuffle(edge_arrival_order)

#     return fractional_matching, edge_arrival_order

