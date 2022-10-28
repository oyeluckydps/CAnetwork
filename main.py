import random
from CAnode import CAnode
from support import *
import warnings
from operators_fast import *
from pathlib import Path
import os
import time
from graphs import *
from CAnetwork import CAnetwork

cwd = Path(os.getcwd())

if __name__ == '__main__':
    # graph = construct_binary_bidir_tree(6)
    # graph_conn = construct_fully_connected_graph(10)
    # graph_6 = construct_tesseract(6, 'binary')
    # node1 = CAnode(1,1)
    # print(node1.__repr__())
    # network = CAnetwork(graph, 'random')
    # network.add_node('NN1', 0, incoming_nodes=[63], outgoing_nodes=[126])
    # network.add_edge('NN1', 0)
    # network.add_edge(0, 'NN1')
    # network.add_node('NN2', 'random', incoming_nodes=[63, 'NN1'], outgoing_nodes=[126, 'NN1'])
    # print(network)
    # network.remove_node('NN1')
    # network.remove_node(63)
    # network.remove_node(126)
    # print(network)


    # graph = construct_tesseract(3)
    # graph = construct_binary_bidir_tree(3)

    TOTAL_TIME_STEPS = 10000
    SIM_CASES = 20
    base_name = "ring2"
    folder_base = cwd / Path(base_name)
    for dim in list(range(3,10)) + list(range(10, 50, 5)) + list(range(50,200,10)):
        folder_dim = folder_base/("dim_"+str(dim))
        all_match_results = {}
        for F_name, F_fun in half_symm_impl.items():
            folder_F_name = folder_dim / ("F_" + F_name)
            for G_name, G_fun in impl.items():
                folder_G_name = folder_F_name / ("G_"+binary(G_name, 4))
                for sim in range(SIM_CASES):
                    file_name = folder_G_name / (str(sim)+".txt")
                    print("Generating : " + str(file_name))
                    graph = construct_ring(dim)
                    network = CAnetwork(graph, 'random', F_fun, G_fun)
                    network.simulate_the_network(range(TOTAL_TIME_STEPS), early_stop=True)
                    parent_folder = file_name.parents[0]
                    parent_folder.mkdir(parents = True, exist_ok=True)
                    network.log_to_file(file_name, match_detail=True)
                    all_match_results[(dim, F_name, binary(G_name, 4), sim)] = (network.match_index, network.last_index)
                    pass
        f = open(folder_base/(str(dim) + ".log"), 'w')
        summary_str = "all_match_results = " + dict_str(all_match_results)
        f.write(summary_str)
        f.close()
    pass


    # dim = 13
    # TOTAL_TIME_STEPS = 10000
    # F_fun = AND
    # G_fun = impl_1010
    # graph = construct_binary_bidir_tree(dim)
    # print(graph)
    # network = CAnetwork(graph, 'random', F_fun, G_fun)
    # start_time = time.time()
    # network.simulate_the_network(range(TOTAL_TIME_STEPS), early_stop=True)
    # end_time = time.time()
    # print(end_time-start_time)
    # print(network.match_index, network.last_index)
    # start_time = time.time()
    # network.log_to_file('check.log')
    # end_time = time.time()
    # print(end_time - start_time)
    # pass