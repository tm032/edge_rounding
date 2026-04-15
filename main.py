from evaluate_schemes import run_experiments

# For selecting which rounding scheme to execute.
from rounding_schemes import SIMULATED_ROUNDING_SCHEME_WITH_IS, SIMULATED_ROUNDING_SCHEME, SIMPLE_ROUNDING_SCHEME, SIMPLE_ROUNDING_SCHEME_FOR_TREE

def get_star_graph_file(n, uniform, order):
    if uniform:
        return f"uniform_star_{n}_order_{order}.json"
    else:
        return f"nonuniform_star_{n}_order_{order}.json"
    
def get_complete_graph_file(n, uniform, order):
    if uniform:
        return f"uniform_complete_{n}_order_{order}.json"
    else:
        return f"nonuniform_complete_{n}_order_{order}.json"
    
def get_bipartite_graph_file(n, m, uniform, order):
    if uniform:
        return f"uniform_bipartite_{n}_{m}_order_{order}.json"
    else:
        return f"nonuniform_bipartite_{n}_{m}_order_{order}.json"
    
def get_tree_graph_file(tree_r, tree_h, uniform, order):
    if uniform:
        return f"uniform_tree_{tree_r}_{tree_h}_order_{order}.json"
    else:
        return f"nonuniform_tree_{tree_r}_{tree_h}_order_{order}.json"


def get_parameter_template_for_graph_file(graph_file, rounding_scheme, c, r, num_sim_instances):
    if "star" in graph_file:
        num_leaves = int(graph_file.split("_")[2])
        average_edge_weight = 1/num_leaves
    
    elif "complete" in graph_file:
        num_vertices = int(graph_file.split("_")[2])
        average_edge_weight = 1/(num_vertices-1)
    
    elif "bipartite" in graph_file:
        num_left_vertices = int(graph_file.split("_")[2])
        num_right_vertices = int(graph_file.split("_")[3])
        average_edge_weight = 1/min(num_left_vertices, num_right_vertices)
    
    elif "tree" in graph_file:
        tree_r = int(graph_file.split("_")[2])
        average_edge_weight = 1/(tree_r+1)

    rounding_scheme_abbv = {
        SIMULATED_ROUNDING_SCHEME_WITH_IS: "is",
        SIMULATED_ROUNDING_SCHEME: "mc",
        SIMPLE_ROUNDING_SCHEME: "si",
        SIMPLE_ROUNDING_SCHEME_FOR_TREE: "tr"
    }

    c_abbv = "c" + str(int(c*100))
    r_abbv = "r" + str(int(r*100))

    experiment_name = graph_file.split(".")[0] + f"_{rounding_scheme_abbv[rounding_scheme]}_{c_abbv}_{r_abbv}_sim{num_sim_instances}"

    parameters = {
        "graph_file": graph_file,
        "c_guarantee": c,
        "experiment_name": experiment_name,
        "average_edge_weight": average_edge_weight,
        "r": r,
        "num_sim_instances": num_sim_instances,
        "rounding_scheme_class": rounding_scheme,
        "parallel": True
    }

    return parameters

def comparing_c_values_experiment(graph_file, rounding_scheme, r=1, num_sim_instances=10000):
    c_values = [0.5, 0.6, 2/3, 0.7, 3/4, 0.8, 0.9, 1.0]
    results = {}
    for c in c_values:
        parameters = get_parameter_template_for_graph_file(graph_file, rounding_scheme, c, r, num_sim_instances)
        result = run_experiments(parameters)
        results[c] = result
    
    return results

def experiment_1():
    # comparing_c_values_experiment(graph_file=get_star_graph_file(20, True, order=0), rounding_scheme=SIMPLE_ROUNDING_SCHEME_FOR_TREE)
    # comparing_c_values_experiment(graph_file=get_star_graph_file(20, True, order=0), rounding_scheme=SIMULATED_ROUNDING_SCHEME, r=1, num_sim_instances=10000)

    # comparing_c_values_experiment(graph_file=get_complete_graph_file(10, True, order=0), rounding_scheme=SIMPLE_ROUNDING_SCHEME)
    # comparing_c_values_experiment(graph_file=get_complete_graph_file(10, True, order=0), rounding_scheme=SIMULATED_ROUNDING_SCHEME, r=1, num_sim_instances=10000)

    # comparing_c_values_experiment(graph_file=get_bipartite_graph_file(10, 10, True, order=0), rounding_scheme=SIMPLE_ROUNDING_SCHEME)
    # comparing_c_values_experiment(graph_file=get_bipartite_graph_file(10, 10, True, order=0), rounding_scheme=SIMULATED_ROUNDING_SCHEME, r=1, num_sim_instances=10000)

    # comparing_c_values_experiment(graph_file=get_tree_graph_file(3, 4, True, order=0), rounding_scheme=SIMPLE_ROUNDING_SCHEME_FOR_TREE)
    # comparing_c_values_experiment(graph_file=get_tree_graph_file(3, 4, True, order=0), rounding_scheme=SIMULATED_ROUNDING_SCHEME, r=1, num_sim_instances=10000)
    pass # Completed experiment 1

def experiment_2():
    star_graph_file = get_star_graph_file(20, False, order=0)
    complete_graph_file = get_complete_graph_file(10, False, order=0)
    bipartite_graph_file = get_bipartite_graph_file(10, 10, False, order=0)
    tree_graph_file = get_tree_graph_file(3, 4, False, order=0)

    comparing_c_values_experiment(graph_file=tree_graph_file, rounding_scheme=SIMULATED_ROUNDING_SCHEME, r=0.6, num_sim_instances=10000)


    for r in [0.4, 0.2, 0.0]:
        # comparing_c_values_experiment(graph_file=complete_graph_file, rounding_scheme=SIMPLE_ROUNDING_SCHEME, r=r)
        # comparing_c_values_experiment(graph_file=complete_graph_file, rounding_scheme=SIMULATED_ROUNDING_SCHEME, r=r, num_sim_instances=10000)

        # comparing_c_values_experiment(graph_file=star_graph_file, rounding_scheme=SIMPLE_ROUNDING_SCHEME_FOR_TREE, r=r)
        # comparing_c_values_experiment(graph_file=star_graph_file, rounding_scheme=SIMULATED_ROUNDING_SCHEME, r=r, num_sim_instances=10000)

        comparing_c_values_experiment(graph_file=bipartite_graph_file, rounding_scheme=SIMPLE_ROUNDING_SCHEME, r=r)
        comparing_c_values_experiment(graph_file=bipartite_graph_file, rounding_scheme=SIMULATED_ROUNDING_SCHEME, r=r, num_sim_instances=10000)

        comparing_c_values_experiment(graph_file=tree_graph_file, rounding_scheme=SIMPLE_ROUNDING_SCHEME_FOR_TREE, r=r)
        comparing_c_values_experiment(graph_file=tree_graph_file, rounding_scheme=SIMULATED_ROUNDING_SCHEME, r=r, num_sim_instances=10000)

if __name__ == "__main__":
    experiment_2()

    # c = 0.6
    # r = 0.7
    # graph_file=get_complete_graph_file(20, False, order=0)
    # # graph_file = get_star_graph_file(40, False, order=0)
    # parameters = get_parameter_template_for_graph_file(graph_file, SIMULATED_ROUNDING_SCHEME, c, r, num_sim_instances=100)
    # result = run_experiments(parameters)

    # parameters = get_parameter_template_for_graph_file(graph_file, SIMULATED_ROUNDING_SCHEME_WITH_IS, c, r, num_sim_instances=100)
    # result = run_experiments(parameters)



    # r = 0.7
    # num_sim_instances = 10000
    # graph_file = get_star_graph_file(10, True, order=0)
    # parameters = get_parameter_template_for_graph_file(graph_file, SIMULATED_ROUNDING_SCHEME_WITH_IS, 0.5, r, num_sim_instances)
    # result = run_experiments(parameters)

    # for v in V:
    #     for uniform in [True, False]:
    #         graph_file = get_star_graph_file(v, uniform, order=0)
    #         comparing_c_values_experiment(graph_file, SIMULATED_ROUNDING_SCHEME_WITH_IS, r=0.7, num_sim_instances=10000)
    
    # for v in V:
    #     for uniform in [True, False]:
    #         graph_file = get_complete_graph_file(v, uniform, order=0)
    #         comparing_c_values_experiment(graph_file, SIMULATED_ROUNDING_SCHEME_WITH_IS, r=0.7, num_sim_instances=10000)

    # for n in V:
    #     for m in U:
    #         for uniform in [True, False]:
    #             graph_file = get_bipartite_graph_file(n, m, uniform, order=0)
    #             comparing_c_values_experiment(graph_file, SIMULATED_ROUNDING_SCHEME_WITH_IS, r=0.7, num_sim_instances=10000)

    # for r in r_tree:
    #     for h in h_tree:
    #         for uniform in [True, False]:
    #             graph_file = get_tree_graph_file(r, h, uniform, order=0)
    #             comparing_c_values_experiment(graph_file, SIMULATED_ROUNDING_SCHEME_WITH_IS, r=0.7, num_sim_instances=10000)

    


