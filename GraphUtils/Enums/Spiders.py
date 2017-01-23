"""
A utility for the enumeration of spider graphs
A spider is a tree with one vertex of degree at least 3 and all others with degree at most 2
"""
import GraphUtils.Graph as Graph

# pylint: disable=bad-continuation,bad-whitespace

class SpiderGenerator(object):
    """ A class that creates spider graphs, with the ability to iterate over the set of spiders """
    _order = None # Stores the order (node count) in the last spider iterated
    _last_leg_lengths = {}  # dict of {edge-length: number-of-legs} (keys, values are all positive)

    def __init__(self, leg_lengths=None):
        """ Initialize the class. if leg lengths"""
        if leg_lengths is not None:
            self._last_leg_lengths = leg_lengths
            order = 1  # (the root node)
            for key, val in leg_lengths.iteritems():
                order += key * val
            self._order = order
        else:
            self._last_leg_lengths = {1: 2}  # not a spider, but ensures the correct "first" spider
            self._order = 3

    def _next_leg_lengths(self):
        """ Returns the dict of leg lengths for the next spider to be generated """
        sorted_lengths = self._last_leg_lengths.keys()
        sorted_lengths.sort()
        maximum = sorted_lengths[-1]
        minimum = sorted_lengths[0]
        assert minimum > 0  # should always be true
        if len(sorted_lengths) > 1:
            second_min = sorted_lengths[1]
        else:
            second_min = float('-inf')

        if maximum is 1:
            # All spiders of the current order have been exhausted
            # build the first spider of the next order
            if self._order + 1 is 4:
                next_legs = {1: 3}
            else:
                next_legs = {self._order-2: 1, 1: 2}

        else:
            next_legs = self._last_leg_lengths.copy()
            new_length = second_min - 1

            if minimum is 1:
                edges_to_add = next_legs[1] + second_min
                next_legs.update({second_min: next_legs[second_min] - 1, 1: 0})

                if second_min is maximum and next_legs[second_min] is 0\
                        and edges_to_add/float(new_length) <= 2:
                    # be careful to always have 3 legs
                    next_legs.update({new_length: 1, edges_to_add - new_length - 1: 1, 1: 1})
                else:
                    next_legs.update({
                        new_length: edges_to_add / new_length, edges_to_add % new_length: 1
                    })
            elif minimum is 2:
                next_legs.update({2: next_legs[2] - 1, 1: 2})
            else:
                next_legs.update({
                    minimum: next_legs[minimum] - 1
                    ,minimum - 1: 1
                    ,1: 1
                })

        # make sure that there are no zero keys or values in the dict
        final_leg_dict = dict((key, val) for key, val in next_legs.iteritems()
                              if val is not 0 and key is not 0)
        return final_leg_dict

    def create_spider(self, leg_lengths):  # pylint: disable=no-self-use
        """ Given a dict of leg lengths, output the corresponding spider Graph """
        spider = Graph.Graph()
        spider. add_node()  # root node
        root_id = 0
        last_node_id = 0
        for length, count in leg_lengths.iteritems():
            for c in range(count):  # pylint: disable=invalid-name,unused-variable
                # attach a new leg
                spider.add_node()
                last_node_id += 1
                spider.add_edge(root_id, last_node_id)
                for i in range(length-1):  # pylint: disable=invalid-name,unused-variable
                    spider.add_node()
                    last_node_id += 1
                    spider.add_edge(last_node_id - 1, last_node_id)
        return spider

    def next(self):
        """ Return the next spider as a Graph object """
        next_lengths = self._next_leg_lengths()
        next_spider = self.create_spider(next_lengths)
        self._order = next_spider.order
        self._last_leg_lengths = next_lengths
        return next_spider
