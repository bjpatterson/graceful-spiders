"""Provides basic graph functionality"""


class Graph(object):
    """ A basic class representing a simple undirected graph """
    _id_next = 0
    node_dict = {}  # {id: label}
    edge_list = []  # (id1, id2) where id1 < id2

    def __init__(self):
        """nothing special required here"""
        pass

    def add_node(self, label=None):
        """adds a new node to the graph and returns the node's id"""
        self.node_dict.update({self._id_next: label})
        self._id_next += 1
        return self._id_next - 1

    def add_edge(self, id1, id2):
        """adds and edge between two nodes if both ids are valid, not equal, and no edge exists"""
        if id1 is not id2 and id1 in self.node_dict and id2 in self.node_dict:
            new_edge = (min(id1, id2), max(id1, id2))
            if new_edge not in self.edge_list:
                self.edge_list.append(new_edge)

    def remove_node(self, node_id):
        """removes a node by id, and all adjacent edges"""
        self.node_dict.pop(node_id)
        self.edge_list =\
            [(id1, id2) for id1, id2 in self.edge_list if id1 is not node_id and id2 is not node_id]

    def remove_edge(self, id1, id2):
        """removes an edge between two node ids it exists"""
        self.edge_list.remove((min(id1, id2), max(id1, id2)))

    def clear(self):
        """resets the graph to its default state"""
        self.node_dict = {}
        self.edge_list = []
        self._id_next = 0
