from support import *
import copy
import numpy

def construct_fully_connected_graph(num_nodes):
    graph = {}
    for i in range(num_nodes):
        graph[i] = list(range(num_nodes))
        graph[i].remove(i)
    return graph

def construct_binary_bidir_tree(depth):
    graph = {i: [] for i in range(2 ** (depth + 1) - 1)}
    for i in range(depth):
        for j in range(2**i-1, 2**(i+1)-1):
            graph[j].append(2*j+1)
            graph[j].append(2*j+2)
            graph[2*j+1].append(j)
            graph[2*j+2].append(j)
    return graph

def construct_chain(length):
    if length < 1:
        return None
    elif length == 1:
        return {0:[0]}
    else:
        graph = {i: [] for i in range(length)}
        graph[0] = [1]
        for i in range(1, length-1):
            graph[i] = [i-1, i+1]
        graph[length-1] = [length-2]
        return graph

def construct_ring(length):
    graph = construct_chain(length)
    graph[0].append(length-1)
    graph[length-1].append(0)
    return graph

def construct_tesseract(dimension, naming_convention = 'number'):
    '''
    Input:
        dimension: Number of dimensions to binary tesseract.
        naming_convention: Either of the values number or binary for binary representation
    '''
    xor_key = [2**i for i in range(dimension)]
    graph = {num: [num^i for i in xor_key] for num in range(2 ** dimension)}
    if naming_convention == 'binary':
        graph = {binary(k, dimension):[binary(j, dimension) for j in v] for k, v in graph.items()}
        return graph
    else:   # Add more naming_conventions here.
        return graph



def remove_node(tree, node):
    for i in tree[node]:
        tree[i].remove(node)
    del tree[node]
    return tree

# def hash_at_node(node, tree):
#     tree_copy = copy.deepcopy(tree)
#     nodes_in_process = [node]
#     hash = []
#     while len(tree_copy) > 0:
#         next_nodes = []
#         next_nodes_count = []
#         for processing_node in nodes_in_process:
#             next_nodes.append(tree_copy[processing_node])
#             next_nodes_count.append(len(tree_copy[processing_node]))
#         for processing_node in nodes_in_process:
#             tree_copy = remove_node(tree_copy, processing_node)
#         sort_index = numpy.argsort(next_nodes_count)
#         hash += [n for (i, n) in sorted(zip(sort_index, next_nodes_count))]
#         next_nodes_sorted = [n for (i, n) in sorted(zip(sort_index, next_nodes))]
#         nodes_in_process = [item for sublist in next_nodes_sorted for item in sublist]
#     return tuple(hash)
def hash_at_node(node, tree):
    tree_copy = copy.deepcopy(tree)
    leafs = copy.deepcopy(tree_copy[node])
    tree_copy = remove_node(tree_copy, node)
    if len(leafs) == 0:
        return (1, )
    elif len(leafs) == 1:
        return (hash_at_node(leafs[0], tree_copy)[0]+1, ) 
    leaf_hashes = []
    for leaf in leafs:
        leaf_hashes.append(hash_at_node(leaf, tree_copy))
    hash_sorted = sorted(leaf_hashes, reverse = True)
    hash = tuple([item for sublist in hash_sorted for item in sublist])
    return hash

def add_tree_node(tree):
    isomorphic_group = {}
    for node, edges in tree.items():
        node_hash = hash_at_node(node, tree)
        if node_hash in isomorphic_group:
            isomorphic_group[node_hash].append(node)
        else:
            isomorphic_group[node_hash] = [node]
    new_node = list(tree.keys())[-1] + 1   # Not really sure if len(tree) is a better idea.
    all_constructed_trees = []
    for node_hash, nodes in isomorphic_group.items():
        node_to_attach = nodes[-1]
        new_tree = copy.deepcopy(tree)
        new_tree[node_to_attach].append(new_node)
        new_tree[new_node] = [node_to_attach]
        all_constructed_trees.append(new_tree)
    return all_constructed_trees


def construct_all_trees(nodes, mode = 'all'):
    all_graphs_size = [0]
    graph = {0 : []}
    all_graphs = [graph]
    working_index = 0
    while (all_graphs_size[working_index] <= nodes) or (working_index < len(all_graphs)-1):
        # Generate tree
        all_trees_size = len(all_graphs)
        new_trees = add_tree_node(all_graphs[working_index])
        all_graphs = add_non_isomorphic_graph(all_graphs, new_trees)
        all_trees_size += [len(all_graphs[-1])]*(len(all_graphs) - all_trees_size)
        working_index += 1
    if mode == 'all':
        return  all_graphs
    elif mode == 'only':
        return {k:v for (k,v) in all_graphs.items() if k==nodes}

if __name__ == '__main__':
    node6_a = {
        0: [1, 2],
        1: [0, 2, 4],
        2: [0, 1, 3],
        3: [2, 4],
        4: [1, 3, 5],
        5: [4]
    }
    node6_b = {
        0: [1],
        1: [0, 2, 4],
        2: [1, 3, 5],
        3: [2, 4],
        4: [1, 3, 5],
        5: [2, 4]
    }
    print(hash_at_node(1, node6_a))
    print(hash_at_node(1, node6_b))