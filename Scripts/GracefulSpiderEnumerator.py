""" Generates all possible graceful spiders in a sane order """

import GraphUtils.Graph as Graph
import time

OUTPATH = 'results/spider_enum_order_{0:0>3}.txt'

def is_unique_graceful_spider(graph):
    """
    Given a graceful graph, detect whether it's a spider.
    (Some special logic detects and rejects certain types of symmetric spiders)
    """
    ds = graph.degree_sequence
    if ds[0] > 2 >= ds[1] and ds[-1] > 0 and graph.component_count is 1:
        # connected graph with a single node of degree > 2 (definition of a spider)
        if graph.order % 2 is 0:  # even-order spiders don't have symmetry issues
            return True
        elif graph.get_degree(graph.order / 2) <= 2:  # non-central branch nodes are not symmetric
            return True
        elif graph.has_edge(0, graph.order - 2):  # choose exactly one edge with label n-2
            return True
        else:
            # technically a graceful spider, but would result in double-counting
            return False

    else:
        return False


def enum_graceful_spiders(partial_graph, next_edge):
    """
    Given a partial graceful labeling, and the next edge label,
    recursively enumerate graceful spiders.
    (use various early-detection rules to prune dead computational branches)
    """
    for i in range(0, partial_graph.order - next_edge):
        n1 = i
        n2 = n1 + next_edge
        if potentially_graceful(partial_graph, n1, n2):
            # add the edge
            partial_graph.add_edge(n1, n2)

            # if that was the last edge, check for gracefulness, and output as needed
            if next_edge is 1:
                if is_unique_graceful_spider(partial_graph):
                    # record enough detail to recreate the spider (edges are sufficient)
                    order = partial_graph.order
                    edges = [e for e in partial_graph.get_edges()]
                    edge_complement = [(order - b - 1, order - a - 1) for (a, b) in edges]
                    with open(OUTPATH.format(order), 'a') as outfile:
                        outfile.write(str(edges))
                        outfile.write('\n')
                        outfile.write(str(edge_complement))
                        outfile.write('\n')
            else:
                enum_graceful_spiders(partial_graph, next_edge - 1)

            # remove the edge before moving back up the computation tree
            partial_graph.remove_edge(n1, n2)


def potentially_graceful(graph, node1, node2):
    """
    given a partial graceful graph and two nodes to connect,
    determine if adding an edge between those nodes results in a still-potentially-graceful spider.
    """

    max_branch_id = (graph.order - 1) / 2  # (larger branch ids found via graceful complement)
    d1 = graph.get_degree(node1)
    d2 = graph.get_degree(node2)
    deg_seq = graph.degree_sequence
    max_deg = deg_seq[0]
    num_zeros = deg_seq.count(0)
    num_ones = deg_seq.count(1)

    if node1 is 0 and node2 is graph.order - 1:  # can't prune the first computational step
        return True
    if num_ones < max_deg:  # there must be a cycle
        return False
    if 2 * num_zeros + num_ones - max_deg < abs(node2 - node1):
        # the graph cannot be fully connected with the remaining number of edges
        return False
    if d1 < 2 and d2 < 2:  # both nodes are non-branching after adding the edge
        return True
    if d1 >= 2 and d2 >= 2:  # both nodes are branching after adding the edge
        return False
    if d1 > 2 or d2 > 2:  # one node was already the branch node, the other remains non-branching
        return True
    if max_deg is 2:  # there is not yet a branch node
        if d1 is 2 and node1 <= max_branch_id:  # node1 is a valid branch node candidate
            return True
        if d2 is 2 and node2 <= max_branch_id:  # node2 is a valid branch node candidate
            return True

    # We've touched on all the possible True cases, so if we've made it here, return False
    return False

if __name__ == '__main__':

    for order in range(4, 15):
        # create an empty graph of the appropriate order
        g = Graph.Graph()
        for i in range(order):
            g.add_node()

        start = time.time()
        enum_graceful_spiders(g, order - 1)
        end = time.time()
        print('finished order {} in {:.3g} seconds'.format(order, end-start))
