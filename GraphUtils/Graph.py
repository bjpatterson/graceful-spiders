"""Provides basic graph functionality"""


class Graph(object):
    """ A basic class representing a simple undirected graph """
    _id_next = 0
    _node_dict = dict()  # {id: label}
    _edge_set = set()  # (id1, id2) where id1 < id2

    def __init__(self):
        """nothing special required here"""
        self.reset()

    @property
    def order(self):
        """define the order of a graph"""
        return len(self._node_dict)

    def add_node(self, label=None):
        """adds a new node to the graph and returns the node's id"""
        self._node_dict.update({self._id_next: label})
        self._id_next += 1
        return self._id_next - 1

    def add_edge(self, node1, node2):
        """adds and edge between two nodes if both ids are valid, not equal, and no edge exists"""
        if node1 is not node2 and node1 in self._node_dict and node2 in self._node_dict:
            new_edge = (min(node1, node2), max(node1, node2))
            self._edge_set.add(new_edge)

    def remove_node(self, node_id):
        """removes a node by id, and all adjacent edges"""
        self._node_dict.pop(node_id)
        self._edge_set = {(node1, node2) for node1, node2 in self._edge_set
                          if node1 is not node_id and node2 is not node_id}

    def remove_edge(self, node1, node2):
        """removes an edge between two node ids it exists"""
        self._edge_set.discard((min(node1, node2), max(node1, node2)))

    def reset(self):
        """resets the graph to its default state"""
        self._node_dict = dict()
        self._edge_set = set()
        self._id_next = 0

    def get_nodes(self):
        """returns a list of node ids in the graph"""
        return self._node_dict.keys()

    def get_node_labels(self):
        """returns a dictionary of node_id: node_label entries for the graph"""
        return self._node_dict

    def get_edges(self):
        """returns a set of edge tuples"""
        return self._edge_set

    def has_node(self, node_id):
        """returns true if a node with given ID exists, false otherwise"""
        return node_id in self._node_dict.keys()

    def has_edge(self, node1, node2):
        """returns true if a given edge exists, false otherwise"""
        return (min(node1, node2), max(node1, node2)) in self._edge_set

    def get_label(self, node_id):
        """returns the label for a given node id"""
        return self._node_dict.get(node_id)

    def set_label(self, node_id, label):
        """sets the label for a given node id"""
        if self.has_node(node_id):
            self._node_dict.update({node_id: label})

    def get_adjacent_nodes(self, node_id):
        """return the set of adjacent node ids from a given node id"""
        adjacent_nodes = set()
        for node1, node2 in self._edge_set:
            if node1 is node_id:
                adjacent_nodes.add(node2)
            elif node2 is node_id:
                adjacent_nodes.add(node1)
        return adjacent_nodes

    def copy(self):
        new_graph = Graph()
        new_graph._id_next = self._id_next
        new_graph._node_dict = self._node_dict.copy()
        new_graph._edge_set = self._edge_set.copy()
        return new_graph
