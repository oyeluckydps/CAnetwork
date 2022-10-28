import random
from CAnode import CAnode
from support import *
import warnings
from operators_fast import *
from pathlib import Path
import os
import time

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
        self.logged_values = ([], [])     #Logger doesn't work if you add or remove node in between of simulation
        self.match_index = None
        self.log_value(-1)

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

    def log_value(self, instance_name = None):
        self.logged_values[1].append(self.network_value_str)
        if instance_name is None:
            instance_name = self.logged_values[0][-1]+1
        self.logged_values[0].append(instance_name)
        self.last_index = instance_name

    def check_redundancy(self):
        try:
            match_indice = self.logged_values[1][:-1].index(self.logged_values[1][-1])
            return self.logged_values[0][match_indice], self.logged_values[0][-1]
        except ValueError:
            return None, self.logged_values[0][-1]

    def step_the_network(self, instance_name = None):
        self.process_network()
        self.enact_value()
        self.log_value(instance_name)

    def simulate_the_network(self, iterator, early_stop = True):
        for t in iterator:
            self.step_the_network(instance_name=t)
            if early_stop:
                match_index, last_index = self.check_redundancy()
                if match_index is not None: # Found a match with last row.
                    self.match_index, self.last_index = match_index, last_index
                    break
        return

    def log_to_file(self, filename, match_detail = True):
        self_string = ''
        graph_string = "Graph representation of the network is:\n" + dict_str(self.network)
        self_string += graph_string
        if match_detail:
            match_string = '*'*len(self) + "\n"
            if self.match_index is not None:
                match_string += "Found a match for last row = " + str(self.last_index) + ", at match row = "\
                + str(self.match_index) +".\n\n"
            else:
                match_string += "No match found!\n\n"
            self_string += match_string
        self_string +=  '*'*len(self) + "\n"
        byte_seq = bytes(self_string, 'utf-8')
        write_bytes_to_file(filename, byte_seq)

        logger_to_file(filename, self.logged_values[1])


    @property
    def network_value(self):
        return [node.value for _, node in self]

    @property
    def network_value_str(self):
        network_str = ''.join([str(node.value) for _, node in self])
        return network_str

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


