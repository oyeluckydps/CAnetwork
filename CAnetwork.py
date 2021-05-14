import random
from CAnode import CAnode
from support import *

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
    graph(length-1).append(0)
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

    def __init__(self, graph = None, node_values = None, incoming_operator=None, post_reg_operator=None, msg = ''):
        if graph is not None:
            self.network = graph
            self.nodes = {}
            self.msg = ''
            for (node_name, edges), value in zip(self.network.items(), node_values):
                self.nodes[node_name] = CAnode(node_name, value, incoming_operator=incoming_operator, post_reg_operator=post_reg_operator)
            for node_name, edges in self.network.items():
                self.nodes[node_name].add_outgoing_nodes([self.nodes[other_end] for other_end in edges])
                for other_end in edges:
                    self.nodes[other_end].add_incoming_nodes(self.nodes[node_name])
        else:
            self.network = {}
            self.nodes = {}

    def add_node(self, name, val, outgoing_nodes = None, incoming_nodes = None, *args, **kwargs):
        '''
        :param name: Name of node to add
        :param val: Value of node to add
        :param outgoing_nodes: list of outgoing nodes
        :param incoming_nodes: lsit of incoming nodes
        :return:
        '''
        # Raise error if name already exists.
        if name in self.nodes.keys():
            raise KeyError

        # Create new node and add it to the network.
        new_node = CAnode(name, val, outgoing_nodes=outgoing_nodes, incoming_nodes=incoming_nodes, *args, **kwargs)
        self.nodes[name] = new_node
        if outgoing_nodes:
            self.network[name] = [node.name for node in outgoing_nodes]
        if incoming_nodes:
            for node in incoming_nodes:
                self.network[node.name].append(name)

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

        # Convert to ndoes if node names are passed in list.
        from_nodes = [self.nodes[node] if type(node) is not CAnode else node for node in from_nodes]
        to_nodes = [self.nodes[node] if type(node) is not CAnode else node for node in to_nodes]

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
        to_list = self.network[name]
        from_list = [name]*len(to_list)
        for from_node_name, to_node_name_list in self.network.items():
            if name in to_node_name_list:
                from_list.append(from_node_name)
                to_list.append(name)

        # Remove the edges
        if to_list and from_list:
            self.remove_edge(from_list, to_list)

        # Remove node from self dictionaries.
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
        if type(node_edge) is not list:
            to_nodes = [node_edge]

        # Convert to ndoes if node names are passed in list.
        from_nodes = [self.nodes[node] if type(node) is not CAnode else node for node in from_nodes]
        to_nodes = [self.nodes[node] if type(node) is not CAnode else node for node in to_nodes]

        # Iterate over the list and remove edge one by one.
        for from_node, to_node in zip(from_nodes, to_nodes):
            if not self.is_edge(from_node, to_node):
                raise ValueError
            from_node.remove_outgoing_nodes(to_node)
            to_node.remove_incoming_nodes(from_node)
            self.network[from_node.name].remove(to_node.name)

            # Check for isolated node and remove it.
            if len(self.network[from_node.name])==0 and \
                all([from_node.name not in to_nodes_list if node_name is not from_node.name else True for node_name, to_nodes_list in self.network.items()]):
                self.remove_node(from_node)

    def set_incoming_operator(self, incoming_operator):
        for _, node in self.nodes.items():
            node.set_incoming_operator(incoming_operator=incoming_operator)

    def set_post_reg_operator(self, post_reg_operator):
        for _, node in self.nodes.items():
            node.set_post_reg_operator(post_reg_operator=post_reg_operator)

    def process_network(self):
        '''
        :return: processing each node of network
        operator on the output of first process and stored value.
        '''
        for _, node in self.nodes.items():
            node.process_node()

    def enact_value(self):
        for _, node in self.nodes.items():
            node.enact_value()

    def step_the_network(self):
        self.process_network()
        self.enact_value()

    def __iter__(self):
        return iter(self.nodes.items())

    def __getitem__(self, item):
        return self.nodes[item]

    def __str__(self, prefix = '', indent = '\t'):
        total_indent = prefix
        message = prefix + self.__repr__() + '\n' + total_indent
        for name, node in self:
            message+=node.__str__(prefix = indent) + '\n' + total_indent
        message = message[:-1]
        return message

    def __repr__(self):
        edges = sum([len(v) for _,v in self.network.items()])
        message = '<'+str(id(self))+': '+str(len(self.nodes))+' nodes, '+str(edges)+' edges'
        if self.msg:
            message += ', msg = ' + self.msg + '>'
        else:
            message += '>'
        return message


if __name__ == '__main__':
    graph = construct_binary_bidir_tree(6)
    # graph_conn = construct_fully_connected_graph(10)
    graph_6 = construct_tesseract(6, 'binary')
    # node1 = CAnode(1,1)
    # print(node1.__repr__())
    network = CAnetwork(graph, [random.randint(0, 1) for i in range(len(graph))])
    pass