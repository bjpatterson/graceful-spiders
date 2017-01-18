"""Provides basic graph functionality"""


class Graph(object):
    """ A basic class representing a simple undirected graph """
    _id_next = 0
    _node_dict = {}  # {id: label}
    _edge_list = []  # (id1, id2) where id1 < id2

    def __init__(self):
        """nothing special required here"""
        self.reset()

    def add_node(self, label=None):
        """adds a new node to the graph and returns the node's id"""
        self._node_dict.update({self._id_next: label})
        self._id_next += 1
        return self._id_next - 1

    def add_edge(self, node1, node2):
        """adds and edge between two nodes if both ids are valid, not equal, and no edge exists"""
        if node1 is not node2 and node1 in self._node_dict and node2 in self._node_dict:
            new_edge = (min(node1, node2), max(node1, node2))
            if new_edge not in self._edge_list:
                self._edge_list.append(new_edge)

    def remove_node(self, node_id):
        """removes a node by id, and all adjacent edges"""
        self._node_dict.pop(node_id)
        self._edge_list = [(node1, node2) for node1, node2 in self._edge_list
                           if node1 is not node_id and node2 is not node_id]

    def remove_edge(self, node1, node2):
        """removes an edge between two node ids it exists"""
        self._edge_list.remove((min(node1, node2), max(node1, node2)))

    def reset(self):
        """resets the graph to its default state"""
        self._node_dict = {}
        self._edge_list = []
        self._id_next = 0

    def get_nodes(self):
        """returns a list of node ids in the graph"""
        return self._node_dict.keys()

    def get_node_labels(self):
        """returns a dictionary of node_id: node_label entries for the graph"""
        return self._node_dict

    def get_edges(self):
        """returns a list of edge tuples"""
        return self._edge_list

    def has_node(self, node_id):
        """returns true if a node with given ID exists, false otherwise"""
        return node_id in self._node_dict.keys()

    def has_edge(self, node1, node2):
        """returns true if a given edge exists, false otherwise"""
        return (min(node1, node2), max(node1, node2)) in self._edge_list

    def get_label(self, node_id):
        """returns the label for a given node id"""
        return self._node_dict.get(node_id)

    def set_label(self, node_id, label):
        """sets the label for a given node id"""
        if self.has_node(node_id):
            self._node_dict.update({node_id: label})
