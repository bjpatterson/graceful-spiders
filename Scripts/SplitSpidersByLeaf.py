"""
Read the outputs from `GracefulSpiderEnumerator`, and segregate the spiders by leaf label
(since spiders have multiple leaves, each spider will show up in multiple output files)
"""

import os

SPIDER_FILE = 'results/spider_enum_order_{:0>3}.txt'
SEPARATED_FOLDER = 'results/order_{0}'
SEPARATED_FILE = 'order_{0:0>3}_leaf_{1:0>3}.txt'


def has_leaf(edge_list, leaf_id):
    return len([edge for edge in edge_list if leaf_id in edge]) == 1


def separate_spiders(order):
    if not os.path.exists(SEPARATED_FOLDER.format(order)):
        os.makedirs(SEPARATED_FOLDER.format(order))
    for line in open(SPIDER_FILE.format(order), 'r').readlines():
        edges = eval("list({})".format(line))
        for leaf_id in range(order):
            if has_leaf(edges, leaf_id):
                filename = SEPARATED_FOLDER + '\\' + SEPARATED_FILE
                with open(filename.format(order, leaf_id), 'a') as outfile:
                    outfile.write(line)


if __name__ == '__main__':
    for i in range(4, 17):
        separate_spiders(i)
