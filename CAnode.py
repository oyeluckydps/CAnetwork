from functools import reduce
from operators import *

PRINT_WIDTH = 70

class CAnode:

    def __init__(self, name, val, outgoing_nodes = None, incoming_nodes = None,
                 incoming_operator=None, post_reg_operator=None):
        '''
        :param val: Initial value of the node.
        :param outgoing_nodes: Nodes that take the value of nodes to other nodes.
        :param incoming_nodes: Nodes that bring the value from other nodes to this node.
        '''
        self.name = name
        self.value = val  #self.value can store the logic, True or False
        self._incoming_operator = incoming_operator
        self._post_reg_operator = post_reg_operator
        if outgoing_nodes is not None:
            self.outgoing_nodes = outgoing_nodes
        else:
            self.outgoing_nodes = []
        if incoming_nodes is not None:
            self.incoming_nodes = incoming_nodes
        else:
            self.incoming_nodes = []

    def add_incoming_nodes(self, nodes_list):
        '''
        :param nodes_list: A list or single node element that has to be added to the incoming list.
        :return: self
        '''
        if type(nodes_list) == list:
            self.incoming_nodes += nodes_list
        else:
            self.incoming_nodes.append(nodes_list)

    def remove_incoming_node(self, node):
        self.incoming_nodes.remove(node)

    def add_outgoing_nodes(self, nodes_list):
        '''
        :param nodes_list: A list or single node element that has to be added to the outgoing list.
        :return: self
        '''
        if type(nodes_list) == list:
            self.outgoing_nodes += nodes_list
        else:
            self.outgoing_nodes.append(nodes_list)

    def remove_outgoing_node(self, node):
        self.outgoing_nodes.remove(node)

    def set_incoming_operator(self, incoming_operator):
        self._incoming_operator = incoming_operator

    def set_post_reg_operator(self, post_reg_operator):
        self._post_reg_operator = post_reg_operator

    def process_node(self):
        '''
        :return: The output after applying incoming_operator on incoming nodes and the post_memory_
        operator on the output of first process and stored value.
        '''
        if self.incoming_nodes:
            incoming_values = [x.value for x in self.incoming_nodes]
            evaluated_value = reduce(lambda x, y: self._incoming_operator(x, y), incoming_values)
        else:
            evaluated_value = None
        self.post_eval_value = self._post_reg_operator(self.value, evaluated_value)
        return self.post_eval_value

    def enact_value(self):
        self.value = self.post_eval_value

    def __str__(self, prefix = '', indent = '\t'):
        all_members = [a for a in dir(self) if not (a.startswith('__') and a.endswith('__')) and not callable(getattr(self, a))]
        total_indent = prefix + indent
        node_name = prefix + "Node: " + str(self.name) + '\n'
        message = node_name
        for member in all_members:
            message += str(member) + ' = ' + str(self.__getattribute__(member)) + '\n'
        message = message[:-1]
        message = message.replace('\n', '\n'+total_indent)
        return message

    def __repr__(self):
        return '<'+str(self.name)+'>'


if __name__ == '__main__':
    n1 = CAnode(1, 1)
    n2 = CAnode(2, 0)
    n1.add_incoming_nodes(n2)
    n1.add_outgoing_nodes(n2)
    n2.add_incoming_nodes(n1)
    n2.add_outgoing_nodes(n1)
    print(n1)
    print(n2)
    n1.set_incoming_operator(OR)
    n1.set_post_reg_operator(XOR)
    n2.set_incoming_operator(OR)
    n2.set_post_reg_operator(XOR)
    print(n1)
    print(n2)
    n1.process_node()
    n2.process_node()
    print(n1)
    print(n2)
    n1.enact_value()
    n2.enact_value()
    print(n1)
    print(n2)