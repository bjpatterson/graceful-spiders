"""
Read the outputs from `SplitSpidersByRoot`, after it has been separated into folders by hand (ew),
outputting the alpha-graceful ones to new files
"""

import os

SEPARATED_FILE = 'results/order_{0}/order_{0:0>3}_root_{1:0>3}.txt'
ALPHA_FOLDER = 'results/alpha_order_{0}'
ALPHA_FILE = 'order_{0:0>3}_root_{1:0>3}.txt'

def is_alpha(edge_list):
    small_nodes = [min(a, b) for (a, b) in edge_list]
    big_nodes = [max(a, b) for (a, b) in edge_list]
    return max(small_nodes) < min(big_nodes)


def separate_alpha_spiders(order, root):
    if not os.path.exists(ALPHA_FOLDER.format(order)):
        os.makedirs(ALPHA_FOLDER.format(order))
    if os.path.exists(SEPARATED_FILE.format(order, root)):  # some files don't!
        out_path = ALPHA_FOLDER + "/" + ALPHA_FILE
        with open(out_path.format(order, root), 'a') as outfile:
            for line in open(SEPARATED_FILE.format(order, root), 'r').readlines():
                edges = eval("list({})".format(line))
                if is_alpha(edges):
                    outfile.write(line)

if __name__ == '__main__':
    for ORDER in range(4, 17):
        for ROOT in range(ORDER):
            separate_alpha_spiders(ORDER, ROOT)
