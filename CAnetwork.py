import random
from CAnode import CAnode
from support import *
import warnings
import pandas as pd
from operators import *
from pathlib import Path
import os

cwd = Path(os.getcwd())

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

class CAnetwork:

    def __init__(self, graph = None, node_values = 'random', incoming_operator=None, post_reg_operator=None, msg = ''):
        '''
        :param graph: A dictionary graph in form of node_name:list_of_outgoing_edge_node.
        :param node_values: Either a list of init_values for nodes in the same order as node_name in the dictionary or
                            an initialization string like 'random'/...
        :param incoming_operator: Pointer to the incoming oprerator function.
        :param post_reg_operator: POint to the post register operator function.
        :param msg: Message to be a part of object display.
        '''
        if graph is not None:
            self.network = graph
            self.nodes = {}
            self.msg = ''
            if type(node_values) is not list:
                if node_values == 'random':
                    node_values = [int(random.random()>=0.5) for i in range(len(graph))]
            for (node_name, edges), value in zip(self.network.items(), node_values):
                self.nodes[node_name] = CAnode(node_name, value, incoming_operator=incoming_operator, post_reg_operator=post_reg_operator)
            for node_name, edges in self.network.items():
                self.nodes[node_name].add_outgoing_nodes([self.nodes[other_end] for other_end in edges])
                for other_end in edges:
                    self.nodes[other_end].add_incoming_nodes(self.nodes[node_name])
        else:
            self.network = {}
            self.nodes = {}
        self.logged_values = pd.DataFrame()
        self.log_value()

    def convert_to_nodes(self, node_list):
        '''
        :param node_list: A list of combination of names and nodes
        :return: The list is converted to a list of nodes only.
        '''
        return [self.nodes[node] if type(node) is not CAnode else node for node in node_list]

    def add_node(self, name, val = 'random', outgoing_nodes = None, incoming_nodes = None, *args, **kwargs):
        '''
        :param name: Name of node to add
        :param val: Value of node to add or a seed to value.
        :param outgoing_nodes: list of outgoing nodes
        :param incoming_nodes: lsit of incoming nodes
        :return:
        '''
        # Raise error if name already exists.
        if name in self.nodes.keys():
            raise KeyError('Node name already exists!')
        if val not in [0, 1]:
            if val == 'random':
                val = random.randint(0, 1)

        # Create new node and add it to the network.
        outgoing_nodes = self.convert_to_nodes(outgoing_nodes)
        incoming_nodes = self.convert_to_nodes(incoming_nodes)
        new_node = CAnode(name, val, outgoing_nodes=None, incoming_nodes=None, *args, **kwargs)
        self.nodes[name] = new_node
        self.network[name] = []

        # Use add edge feature here.
        from_list = [i.name for i in incoming_nodes] + [name]*len(outgoing_nodes)
        to_list = [name]*len(incoming_nodes) + [i.name for i in outgoing_nodes]
        self.add_edge(from_list, to_list)

    def is_edge(self, node, to_node):
        return to_node.name in self.network[node.name]

    def add_edge(self, node, node_edge, dir = 'uni'):
        '''
        :param node: The node from which edge starts
        :param node_edge:  The node to whcih edge ends
        :param dir: uni/bi for unidirectional/bidirectional edge.
        :return:
        '''
        # If single node is passed, make a list out of lt.
        if type(node) is not list:
            node = [node]
        if type(node_edge) is not list:
            node_edge = [node_edge]
        if dir == 'bi':
            from_nodes = node + node_edge
            to_nodes = node_edge + node
        else:
            from_nodes = node
            to_nodes = node_edge

        # Convert to ndoes if node names are passed in list.
        from_nodes = self.convert_to_nodes(from_nodes)
        to_nodes = self.convert_to_nodes(to_nodes)

        # Iterate over lists to add edges.
        for from_node, to_node in zip(from_nodes, to_nodes):
            if self.is_edge(from_node, to_node):
                continue
            from_node.add_outgoing_nodes(to_node)
            to_node.add_incoming_nodes(from_node)
            self.network[from_node.name].append(to_node.name)

    def remove_node(self, node):
        '''
        :param node: Node/Node name to remove
        Remove all edges from and to node one by one.
        :return:
        '''
        # Node if node name is passed
        node = node if type(node) is CAnode else self.nodes[node]
        name = node.name

        # Prepare list of edges to remove
        to_list = [i for i in self.network[name]]
        from_list = [name]*len(to_list)
        for from_node_name, to_node_name_list in self.network.items():
            if from_node_name == name:
                continue
            if name in to_node_name_list:
                from_list.append(from_node_name)
                to_list.append(name)

        # Remove the edges
        if to_list and from_list:
            self.remove_edge(from_list, to_list)
        else:
            # If there is no edge to remove, remove node from self dictionaries.
            del self.network[name]
            del self.nodes[name]


    def remove_edge(self, node, node_edge):
        '''
        :param node: The node from which edge starts
        :param node_edge: The node to whcih edge ends
        :return:
        '''
        # If single node is passed, make a list out of lt.
        if type(node) is not list:
            from_nodes = [node]
        else:
            from_nodes = node
        if type(node_edge) is not list:
            to_nodes = [node_edge]
        else:
            to_nodes = node_edge

        # Convert to ndoes if node names are passed in list.
        from_nodes = self.convert_to_nodes(from_nodes)
        to_nodes = self.convert_to_nodes(to_nodes)

        # Iterate over the list and remove edge one by one.
        for from_node, to_node in zip(from_nodes, to_nodes):
            if not self.is_edge(from_node, to_node):
                raise ValueError('Edge does not exist!')
            from_node.remove_outgoing_node(to_node)
            to_node.remove_incoming_node(from_node)
            self.network[from_node.name].remove(to_node.name)

            # Check for isolated node and remove it.
            # Introducing a known bug here. Even if non-disconnected node is called with remove_node function, it would result in FLoating node warning.
            # The following code only removes isolated nodes, but it cannot take care of bifurcated graph.
            if len(self.network[from_node.name])==0 and \
                all([from_node.name not in to_nodes_list if node_name is not from_node.name else True for node_name, to_nodes_list in self.network.items()]):
                msg = 'Removing a floating node! Node = ' + from_node.__repr__()
                warnings.warn(msg)
                self.remove_node(from_node)
            if len(self.network[to_node.name])==0 and \
                all([to_node.name not in to_nodes_list if node_name is not to_node.name else True for node_name, to_nodes_list in self.network.items()]):
                msg = 'Removing a floating node! Node = ' + to_node.__repr__()
                warnings.warn(msg)
                self.remove_node(to_node)

    def set_incoming_operator(self, incoming_operator):
        for _, node in self:
            node.set_incoming_operator(incoming_operator=incoming_operator)

    def set_post_reg_operator(self, post_reg_operator):
        for _, node in self:
            node.set_post_reg_operator(post_reg_operator=post_reg_operator)

    def process_network(self):
        '''
        :return: processing each node of network
        operator on the output of first process and stored value.
        '''
        for _, node in self:
            node.process_node()

    def enact_value(self):
        for _, node in self:
            node.enact_value()
        return self.network_value

    def log_value(self, instance_name = None):
        s = pd.Series({name:value for (name, _), value in zip(self.nodes.items(), self.network_value)})
        if instance_name:
            s.name = instance_name
            self.logged_values = self.logged_values.append(s)
        else:
            self.logged_values = self.logged_values.append(s, ignore_index=True)

    def step_the_network(self, instance_name = None):
        self.process_network()
        self.enact_value()
        self.log_value(instance_name)
        return self.network_value

    def log_to_file(self, filename):
        self_string = self.__str__() + "\n\n\n" + '*'*len(self) + "\n"
        byte_seq = bytes(self_string, 'utf-8')
        write_bytes_to_file(filename, byte_seq)
        byte_seq = df_to_bianryFile(self.logged_values)
        write_bytes_to_file(filename, byte_seq)

    @property
    def network_value(self):
        network_value = []
        for _, node in self:
            network_value.append(node.value)
        return network_value

    def __iter__(self):
        return iter(self.nodes.items())

    def __getitem__(self, item):
        return self.nodes[item]

    def __setitem__(self, key, value):
        self.nodes[key] = value

    def __len__(self):
        return len(self.nodes)

    def __str__(self, prefix = '', indent = '\t'):
        total_indent = prefix
        message = prefix + self.__repr__() + '\n' + total_indent
        for name, node in self:
            message+=node.__str__(prefix = indent) + '\n' + total_indent
        message = message[:-1]
        return message

    def __repr__(self):
        edges = sum([len(v) for _,v in self.network.items()])
        message = '<'+str(id(self))+': '+str(len(self))+' nodes, '+str(edges)+' edges'
        if self.msg:
            message += ', msg = ' + self.msg + '>'
        else:
            message += '>'
        return message


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


    SIM_CASES = 10
    folder_base = cwd / Path("tesseract")
    for dim in range(3, 8):
        folder_dim = folder_base/("dim_"+str(dim))
        for F_name, F_fun in half_symm_impl.items():
            folder_F_name = folder_dim / ("F_" + F_name)
            for G_name, G_fun in impl.items():
                folder_G_name = folder_F_name / ("G_"+binary(G_name, 4))
                for sim in range(SIM_CASES):
                    file_name = folder_G_name / (str(sim)+".txt")
                    graph = construct_tesseract(dim)
                    network = CAnetwork(graph, 'random', F_fun, G_fun)
                    for time in range(1000):
                        network.step_the_network()
                    parent_folder = file_name.parents[0]
                    parent_folder.mkdir(parents = True, exist_ok=True)
                    network.log_to_file(file_name)
                    pass
    pass