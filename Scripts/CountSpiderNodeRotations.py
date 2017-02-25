""" Using outputs from other scripts, check spiders for index-rotatableness """

import os

BASIC_SPIDER_FILE = 'results/spider_enum_order_{0:0>3}.txt'
BASIC_SUMMARY_FILE = 'results/node_rotation_counts_{0:0>3}.txt'

ALPHA_ROOTED_SPIDER_FILE = 'results/alpha_order_{0}/order_{0:0>3}_root_{1:0>3}.txt'
ALPHA_SUMMARY_FILE = 'results/alpha_rotation_counts_{0:0>3}.txt'


def detect_root(edge_list):
    """given an edge set for a spider, return the root node's label"""
    for node in range(len(edge_list) + 1):
        if len([(a, b) for (a, b) in edge_list if a is node or b is node]) > 2:
            return node
    return -1


def leg_length(root, start_edge, edge_list):
    """counts the number of edges in the path extending from a given start edge"""
    length = 0
    prev_node = root
    prev_edge = start_edge
    while prev_edge is not None:
        length += 1
        prev_node = [node for node in prev_edge if node is not prev_node].pop()
        temp = [edge for edge in edge_list if prev_node in edge and edge is not prev_edge]
        if len(temp) > 0:
            prev_edge = temp.pop()
        else:
            prev_edge = None
    return length


def detect_isomorphism(edge_list, root_id=None):
    """given an edge set for a spider, return a sorted list of its leg lengths"""
    edge_lengths = []
    if root_id is None:
        root = detect_root(edge_list)
    else:
        root = root_id

    for edge in [a for a in edge_list if root in a]:
        edge_lengths.append(leg_length(root, edge, edge_list))
    edge_lengths.sort(reverse=True)
    return edge_lengths


def get_node_positions(edges):
    """
    given an edge set, returns [(edge_lengths, node_id, pos_in_leg, leg_length)] for each node
    (the root node is denoted as length = 0, pos = 0)
    """
    positions = []
    root = detect_root(edges)
    iso = detect_isomorphism(edges, root)
    start_edges = [edge for edge in edges if root in edge]
    positions.append((repr(iso), root, 0, 0))
    for edge in start_edges:
        new_nodes = []
        length = 0
        prev_node = root
        prev_edge = edge
        while prev_edge is not None:
            length += 1
            prev_node = [node for node in prev_edge if node is not prev_node].pop()
            new_nodes.append(prev_node)
            temp = [edge for edge in edges if prev_node in edge and edge is not prev_edge]
            if len(temp) > 0:
                prev_edge = temp.pop()
            else:
                prev_edge = None
        for i in range(len(new_nodes)):
            positions.append((repr(iso), new_nodes[i], i+1, length))
    return positions


def count_rotations(order):
    counts = dict()  # {(edge_lengths, node_id, leg_length, pos_in_leg): count}
    for line in open(BASIC_SPIDER_FILE.format(order), 'r').readlines():
        edges = eval("list({})".format(line))
        node_stats = get_node_positions(edges)
        for stat in node_stats:
            if stat in counts:
                counts[stat] += 1
            else:
                counts.update({stat: 1})

    with open(BASIC_SUMMARY_FILE.format(order), 'w') as outfile:
        outfile.write('edge_lengths;node_id;leg_length;pos_in_leg;count\n')
        for (details, count) in counts.iteritems():
            outfile.write('{};{};{};{};{}\n'
                .format(details[0], details[1], details[2], details[3], count))


def count_alpha_rotations(order):
    counts = dict()  # {(edge_lengths, node_id, leg_length, pos_in_leg): count}
    for root in range(order):
        if os.path.exists(ALPHA_ROOTED_SPIDER_FILE.format(order, root)):
            for line in open(ALPHA_ROOTED_SPIDER_FILE.format(order, root), 'r').readlines():
                edges = eval("list({})".format(line))
                node_stats = get_node_positions(edges)
                for stat in node_stats:
                    if stat in counts:
                        counts[stat] += 1
                    else:
                        counts.update({stat: 1})

    with open(ALPHA_SUMMARY_FILE.format(order), 'w') as outfile:
        outfile.write('edge_lengths;node_id;leg_length;pos_in_leg;count\n')
        for (details, count) in counts.iteritems():
            outfile.write('{};{};{};{};{}\n'
                .format(details[0], details[1], details[2], details[3], count))


if __name__ == '__main__':
    for order in range(4, 17):
        count_rotations(order)
        #count_alpha_rotations(order)
