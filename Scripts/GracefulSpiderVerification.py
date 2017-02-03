import GraphUtils.Enums.Spiders as se
import GraphUtils.Checkers.GracefulChecker as gc

last_checked = {1: 2}

enum = se.SpiderGenerator(last_checked)
checker = gc.GracefulChecker()

current_spider = enum.next()
current_order = current_spider.order

outfile = open('Results/spiders_order_{0:0>3}.txt'.format(current_order), 'w')

while(current_order < 20):
    graceful_spider = checker.find_graceful_labeling(current_spider)
    if graceful_spider is None:
        # if no graceful labeling exists, print the graph's details to file for investigation
        outfile.write('ERROR(NOT GRACEFUL):\n\tcode = {},\n\tnodes = {},\n\tedges = {}\n'.format(
            enum._last_leg_lengths
            ,current_spider.get_nodes()
            ,current_spider.get_edges()
        ))
    else:
        # if a graceful labeling was found, print its details
        outfile.write('GRACEFUL:\n\tcode = {},\n\tnodes = {},\n\tedges = {}\n'.format(
            enum._last_leg_lengths
            ,graceful_spider.get_node_labels()
            ,graceful_spider.get_edges()
        ))

        if graceful_spider.get_label(0) is not 0:
            print 'Spider with no root label 0 possible. code = {}'.format(enum._last_leg_lengths)

    current_spider = enum.next()
    if current_spider.order is not current_order:
        outfile.write('END OF ENUMERATION FOR SPIDERS WITH ORDER {0:0>3}\n'.format(current_order))
        current_order = current_spider.order
        outfile.close()
        outfile = open('Results/spiders_order_{0:0>3}.txt'.format(current_order), 'w')
