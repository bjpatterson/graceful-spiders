"""Provides basic graph functionality"""
import copy

class Graph(object):
    """ A basic class representing a simple undirected graph """
    _id_next = 0
    _node_dict = dict()  # {id: label}
    _edge_set = set()  # (id1, id2) where id1 < id2
    _degrees = []

    def __init__(self):
        """nothing special required here"""
        self.reset()

    @property
    def order(self):
        """define the order of a graph"""
        return len(self._node_dict)

    @property
    def degree_sequence(self):
        """return the degree sequence of a graph"""
        deg_seq = [d for d in self._degrees if d is not None]
        deg_seq.sort(reverse=True)
        return deg_seq

    @property
    def component_count(self):
        """
        return the number of connected components in a graph.
        if the graph is empty, return 0.
        (implementation uses a breadth-first search to identify connected components.)
        """
        unmarked_nodes = self.get_nodes()
        nodes_to_search = list()
        components = 0
        while len(unmarked_nodes) > 0:
            components += 1
            root = min(unmarked_nodes)
            nodes_to_search.append(root)
            unmarked_nodes.remove(root)
            while len(nodes_to_search) > 0:
                curr_node = nodes_to_search.pop()
                for node in self.get_adjacent_nodes(curr_node):
                    if node in unmarked_nodes:
                        unmarked_nodes.remove(node)
                        nodes_to_search.append(node)
        return components

    def add_node(self, label=None):
        """adds a new node to the graph and returns the node's id"""
        self._node_dict.update({self._id_next: label})
        self._degrees.append(0)
        self._id_next += 1
        return self._id_next - 1

    def add_edge(self, node1, node2):
        """adds and edge between two nodes if both ids are valid, not equal, and no edge exists"""
        if node1 is not node2 and node1 in self._node_dict and node2 in self._node_dict:
            new_edge = (min(node1, node2), max(node1, node2))
            self._edge_set.add(new_edge)
            self._degrees[node1] += 1
            self._degrees[node2] += 1

    def remove_node(self, node_id):
        """removes a node by id, and all adjacent edges"""
        self._node_dict.pop(node_id)
        for node in self.get_adjacent_nodes(node_id):
            self._degrees[node] -= 1
        self._degrees[node_id] = None
        self._edge_set = {(node1, node2) for node1, node2 in self._edge_set
                          if node1 is not node_id and node2 is not node_id}

    def remove_edge(self, node1, node2):
        """removes an edge between two node ids it exists"""
        self._edge_set.discard((min(node1, node2), max(node1, node2)))
        self._degrees[node1] -= 1
        self._degrees[node2] -= 1

    def reset(self):
        """resets the graph to its default state"""
        self._node_dict = dict()
        self._edge_set = set()
        self._degrees = []
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

    def get_degree(self, node_id):
        """return the degree of a given node_id. (return None if id doesn't exist.)"""
        if node_id >= len(self._degrees):
            return None
        else:
            return self._degrees[node_id]

    def copy(self):
        """return a copy of the current graph."""
        new_graph = copy.deepcopy(self)
        return new_graph
