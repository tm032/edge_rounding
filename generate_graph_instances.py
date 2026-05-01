from graph import BipartiteGraph, CompleteGraph, StarGraph, TreeGraph

uniform_lb = 0.2
uniform_ub = 0.8

def generate_star_graphs(seed):
    num_leaves = [10, 20, 40]
    for n in num_leaves:
        balanced_star_graph = StarGraph(num_leaves=n)
        balanced_star_graph.set_uniform_edge_weights(1/n)
        
        # No need to randomize edge arrival order for star graphs since all edges are symmetric.
        balanced_star_graph.randomize_edge_arrival_order(seed=0)  # Randomize edge arrival order once for the unbalanced star graph
        balanced_star_graph.export_to_json(f"uniform_star_{n}_order_0.json")

        unbalanced_star_graph = StarGraph(num_leaves=n)
        unbalanced_star_graph.set_unbalanced_edge_weights(uniform_lb, uniform_ub, seed=seed)

        for i in range(5):  # Randomize edge arrival order multiple times to get different instances
            unbalanced_star_graph.randomize_edge_arrival_order(seed=seed+i)
            unbalanced_star_graph.export_to_json(f"nonuniform_star_{n}_order_{i}.json")

def generate_complete_graphs(seed):
    num_vertices = [10, 20, 40]
    for n in num_vertices:
        balanced_complete_graph = CompleteGraph(num_vertices=n)
        balanced_complete_graph.set_uniform_edge_weights(1/(n-1))

        for i in range(5):  # Randomize edge arrival order multiple times to get different instances
            balanced_complete_graph.randomize_edge_arrival_order(seed=2*seed+i)
            balanced_complete_graph.export_to_json(f"uniform_complete_{n}_order_{i}.json")

        unbalanced_complete_graph = CompleteGraph(num_vertices=n)
        unbalanced_complete_graph.set_unbalanced_edge_weights(uniform_lb, uniform_ub, seed=seed)
        for i in range(5):  # Randomize edge arrival order multiple times to get different instances
            unbalanced_complete_graph.randomize_edge_arrival_order(seed=seed+i)
            unbalanced_complete_graph.export_to_json(f"nonuniform_complete_{n}_order_{i}.json")

def generate_bipartite_graphs(seed):
    num_left_vertices = [10, 20, 30]
    num_right_vertices = [10, 20, 30]
    for n in num_left_vertices:
        for m in num_right_vertices:
            balanced_bipartite_graph = BipartiteGraph(num_left_vertices=n, num_right_vertices=m)
            balanced_bipartite_graph.set_uniform_edge_weights(1/m)
            for i in range(5):  # Randomize edge arrival order multiple times to get different instances
                balanced_bipartite_graph.randomize_edge_arrival_order(seed=2*seed+i)
                balanced_bipartite_graph.export_to_json(f"uniform_bipartite_{n}_{m}_order_{i}.json")

            unbalanced_bipartite_graph = BipartiteGraph(num_left_vertices=n, num_right_vertices=m)
            unbalanced_bipartite_graph.set_unbalanced_edge_weights(uniform_lb, uniform_ub, seed=seed)
            for i in range(5):  # Randomize edge arrival order multiple times to get different instances
                unbalanced_bipartite_graph.randomize_edge_arrival_order(seed=seed+i)
                unbalanced_bipartite_graph.export_to_json(f"nonuniform_bipartite_{n}_{m}_order_{i}.json")

def generate_tree_graphs(seed):
    r_values = [2, 3, 4]
    h_values = [3, 4, 5]
    for r in r_values:
        for h in h_values:
            balanced_tree_graph = TreeGraph(r=r, h=h)
            balanced_tree_graph.set_uniform_edge_weights(1/(r+1))
            for i in range(5):  # Randomize edge arrival order multiple times to get different instances
                balanced_tree_graph.randomize_edge_arrival_order(seed=2*seed + i)
                balanced_tree_graph.export_to_json(f"uniform_tree_{r}_{h}_order_{i}.json")

            unbalanced_tree_graph = TreeGraph(r=r, h=h)
            unbalanced_tree_graph.set_unbalanced_edge_weights(uniform_lb, uniform_ub, seed=seed)
            for i in range(5):  # Randomize edge arrival order multiple times to get different instances
                unbalanced_tree_graph.randomize_edge_arrival_order(seed=seed+i)
                unbalanced_tree_graph.export_to_json(f"nonuniform_tree_{r}_{h}_order_{i}.json")


if __name__ == "__main__":
    # generate_star_graphs(seed=1)
    # generate_complete_graphs(seed=103)
    generate_bipartite_graphs(seed=42)
    # generate_tree_graphs(seed=54)