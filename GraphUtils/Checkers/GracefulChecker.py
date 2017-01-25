""" Tools for checking graph gracefulness """


class GracefulChecker(object):
    """ A class for determining whether a given graph is graceful or not """

    def find_labeling(self, graph):
        """
        Given an input graph, output its 'first' graceful labeling, if one exists
        (deterministic, but arbitrary)
        """
        graph_copy = graph.copy()
        nodes = graph_copy.get_nodes()
        nodes.sort()  # just in case
        for node in nodes:
            graph_copy.set_label(node, None)

        edges = graph_copy.get_edges()
        node_labels = set(range(len(edges) + 1))
        edge_labels = set(range(1, len(edges) + 1))

        return self._find_labeling_from_partial(graph_copy, nodes, node_labels, edge_labels)

    def _find_labeling_from_partial(self, graph, unlabeled_nodes, node_labels, edge_labels):
        """
        Given a partially-gracefully-labelled graph, and some info about remaining options,
        Recursively and deterministically find a gracefully labeled tree, and return it.
        (If no tree exists from the given starting point, return None)

        :param graph: partially labeled GraphUtils.Graph.Graph() object
        :param unlabeled_nodes: a list of node IDs that have not yet been labeled
        :param node_labels: a set of the remaining possible node labels
        :param edge_labels: a set of the remaining (required) edge labels
        :return: gracefully labeled GraphUtils.Graph.Graph() object, or None, if none exist
        """

        for label in node_labels:
            # assign an unused label to an unlabeled node
            graph.set_label(unlabeled_nodes[0], label)
            n_labels = node_labels.copy()  # remaining (potential) node labels
            n_labels.remove(label)
            e_labels = edge_labels.copy()  # remaining (required) edge labels
            try:
                for neighbor in graph.get_adjacent_nodes(unlabeled_nodes[0]):
                    neighbor_label = graph.get_label(neighbor)
                    if neighbor_label is not None:
                        induced_label = abs(neighbor_label - label)
                        e_labels.remove(induced_label)  # will throw an error if missing

                if len(unlabeled_nodes[1:]) is 0:
                    # if the labeling is complete, return the labeled graph
                    return graph
                elif max(e_labels) > max(max(n_labels), len(graph._edge_set) - min(n_labels)):
                    # if the remaining node labels make the largest edge label impossible, continue
                    continue
                else:
                    # recurse on the new partial labeling
                    result = self._find_labeling_from_partial(
                        graph.copy(), unlabeled_nodes[1:], n_labels, e_labels)
                    if result is not None:
                        return result
            except KeyError:
                # if a duplicate induced edge is found, skip to the next iteration
                pass

        # No graceful labeling exists from the starting point, restore graph and return None
        graph.set_label(unlabeled_nodes[0], None)
        return None
