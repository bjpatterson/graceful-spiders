"""
Read the outputs from `GracefulSpiderEnumerator`, and segregate the spiders by root label
"""

import os

SPIDER_FILE = 'results/spider_enum_order_{:0>3}.txt'
SEPARATED_FOLDER = 'results/order_{0}'
SEPARATED_FILE = 'order_{0:0>3}_root_{1:0>3}.txt'

def detect_root(edge_list):
    for i in range(len(edge_list) + 1):
        if len([(a, b) for (a, b) in edge_list if a is i or b is i]) > 2:
            return i
    return -1


def separate_spiders(order):
    for line in open(SPIDER_FILE.format(order), 'r').readlines():
        edges = eval("list({})".format(line))
        root = detect_root(edges)
        if not os.path.exists(SEPARATED_FOLDER.format(order)):
            os.makedirs(SEPARATED_FOLDER.format(order))
        out_path = SEPARATED_FOLDER + "/" + SEPARATED_FILE
        with open(out_path.format(order, root), 'a') as outfile:
            outfile.write(line)

if __name__ == '__main__':
    for i in range(4, 6):
        separate_spiders(i)
