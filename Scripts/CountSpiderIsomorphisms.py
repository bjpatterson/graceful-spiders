"""
Read the data outputs from [other related scripts], count the number of each spider isomorphism
"""

import os
import operator

BASIC_SPIDER_FILE = 'results/spider_enum_order_{:0>3}.txt'
BASIC_SUMMARY_FOLDER = 'results'
BASIC_SUMMARY_FILE = 'iso_count_{0:0>3}.txt'

ROOTED_SPIDER_FILE = 'order_{0:0>3}_root_{1:0>3}.txt'
ROOTED_SPIDER_FOLDER = 'results/order_{0}'
ROOTED_SUMMARY_FILE = 'iso_count_order_{0:0>3}_root_{1:0>3}.txt'

ALPHA_ROOTED_SPIDER_FILE = 'order_{0:0>3}_root_{1:0>3}.txt'
ALPHA_ROOTED_SPIDER_FOLDER = 'results/alpha_order_{0}'
ALPHA_ROOTED_SUMMARY_FILE = 'iso_count_order_{0:0>3}_root_{1:0>3}.txt'

LEAF_SUMMARY_FILE = 'iso_leaf_count_order_{0:0>3}.txt'
ALPHA_LEAF_SUMMARY_FILE = 'alpha_leaf_count_order_{0:0>3}.txt'


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


def count_isomorphisms(order):
    counts = dict()
    if not os.path.exists(BASIC_SUMMARY_FOLDER):
        os.makedirs(BASIC_SUMMARY_FOLDER)

    for line in open(BASIC_SPIDER_FILE.format(order), 'r').readlines():
        edges = eval("list({})".format(line))
        isomorphism = detect_isomorphism(edges)
        if repr(isomorphism) in counts:
            counts[repr(isomorphism)] += 1
        else:
            counts.update({repr(isomorphism): 1})

    all_isos = [(key, val) for key, val in counts.iteritems()]
    all_isos.sort(key=operator.itemgetter(1), reverse=True)

    outfile = BASIC_SUMMARY_FOLDER + "/" + BASIC_SUMMARY_FILE
    with open(outfile.format(order), 'w') as outfile:
        for iso in all_isos:
            outfile.write("{}: {}\n".format(iso[1], iso[0]))


def spider_has_leaf(edges, leaf_id):
    return len([edge for edge in edges if leaf_id in edge]) == 1


def count_leaf_isomorphisms(order):
    counts = dict()
    for line in open(BASIC_SPIDER_FILE.format(order), 'r').readlines():
        edges = eval("list({})".format(line))
        isomorphism = detect_isomorphism(edges)
        for label in range(order):
            if spider_has_leaf(edges, label):
                if (repr(isomorphism), label) in counts:
                    counts[(repr(isomorphism), label)] += 1
                else:
                    counts.update({(repr(isomorphism), label): 1})

    all_isos = [(key, val) for key, val in counts.iteritems()]
    all_isos.sort(key=operator.itemgetter(1), reverse=True)

    outfile = BASIC_SUMMARY_FOLDER + "/" + LEAF_SUMMARY_FILE
    with open(outfile.format(order), 'w') as outfile:
        outfile.write('isomorphism;leaf_label;count\n')
        for iso in all_isos:
            outfile.write("{};{};{}\n".format(iso[0][0], iso[0][1], iso[1]))


def count_leaf_alpha_isos(order):
    counts = dict()
    file_path = ALPHA_ROOTED_SPIDER_FOLDER + "\\" + ALPHA_ROOTED_SPIDER_FILE
    for root in range(order):
        if os.path.exists(file_path.format(order, root)):
            for line in open(file_path.format(order, root), 'r').readlines():
                edges = eval("list({})".format(line))
                isomorphism = detect_isomorphism(edges, root)
                for label in range(order):
                    if spider_has_leaf(edges, label):
                        if (repr(isomorphism), label) in counts:
                            counts[(repr(isomorphism), label)] += 1
                        else:
                            counts.update({(repr(isomorphism), label): 1})

    all_isos = [(key, val) for key, val in counts.iteritems()]
    all_isos.sort(key=operator.itemgetter(1), reverse=True)

    outfile_path = BASIC_SUMMARY_FOLDER + "/" + ALPHA_LEAF_SUMMARY_FILE
    with open(outfile_path.format(order), 'w') as outfile:
        outfile.write('isomorphism;leaf_label;count\n')
        for iso in all_isos:
            outfile.write("{};{};{}\n".format(iso[0][0], iso[0][1], iso[1]))


def count_rooted_isomorphisms(order, root):
    counts = dict()
    file_path = ROOTED_SPIDER_FOLDER + "\\" + ROOTED_SPIDER_FILE
    if os.path.exists(file_path.format(order, root)):
        for line in open(file_path.format(order, root), 'r').readlines():
            edges = eval("list({})".format(line))
            isomorphism = detect_isomorphism(edges, root)
            if repr(isomorphism) in counts:
                counts[repr(isomorphism)] += 1
            else:
                counts.update({repr(isomorphism): 1})

        all_isos = [(key, val) for key, val in counts.iteritems()]
        all_isos.sort(key=operator.itemgetter(1), reverse=True)

        outfile = ROOTED_SPIDER_FOLDER + "/" + ROOTED_SUMMARY_FILE
        with open(outfile.format(order, root), 'w') as outfile:
            for iso in all_isos:
                outfile.write("{}: {}\n".format(iso[1], iso[0]))


def count_alpha_rooted_isomorphisms(order, root):
    counts = dict()
    file_path = ALPHA_ROOTED_SPIDER_FOLDER + "\\" + ALPHA_ROOTED_SPIDER_FILE
    if os.path.exists(file_path.format(order, root)):
        for line in open(file_path.format(order, root), 'r').readlines():
            edges = eval("list({})".format(line))
            isomorphism = detect_isomorphism(edges, root)
            if repr(isomorphism) in counts:
                counts[repr(isomorphism)] += 1
            else:
                counts.update({repr(isomorphism): 1})

        all_isos = [(key, val) for key, val in counts.iteritems()]
        all_isos.sort(key=operator.itemgetter(1), reverse=True)

        outfile = ALPHA_ROOTED_SPIDER_FOLDER + "/" + ALPHA_ROOTED_SUMMARY_FILE
        with open(outfile.format(order, root), 'w') as outfile:
            for iso in all_isos:
                outfile.write("{}: {}\n".format(iso[1], iso[0]))


if __name__ == '__main__':
    for order in range(4, 17):
        # count_isomorphisms(order)

        # for root in range(order):
        #     count_rooted_isomorphisms(order, root)

        # for root in range(order):
        #     count_alpha_rooted_isomorphisms(order, root)

        # count_leaf_isomorphisms(order)

        count_leaf_alpha_isos(order)
