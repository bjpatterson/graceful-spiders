"""Unit tests for GraphUtils.Enums.Spiders.py"""

import pytest
import GraphUtils.Enums.Spiders as spdr


def test_next_leg_lengths():
    gen = spdr.SpiderGenerator({1:4})
    assert gen._next_leg_lengths() == {3: 1, 1: 2}
    gen.next()
    assert gen._next_leg_lengths() == {2: 2, 1: 1}
    gen.next()
    assert gen._next_leg_lengths() == {2: 1, 1: 3}
    gen.next()
    assert gen._next_leg_lengths() == {1: 5}
    for i in range(100):
        gen.next()
        assert (sum(val for key, val in gen._next_leg_lengths().iteritems()) > 2)  # assures 3+ legs


def test_create_spider():
    gen = spdr.SpiderGenerator()
    spi = gen.create_spider({1: 5})
    assert spi.order is 6
    for edge in spi.get_edges():
        assert edge in [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
    spi = gen.create_spider({10: 1, 1: 10})
    assert spi.order is 21
    leg_count = 0
    for edge in spi.get_edges():
        if 0 in edge:
            leg_count += 1
    assert leg_count is 11


def test_next():
    gen = spdr.SpiderGenerator()
    order_counts = {}
    expected_order_counts = {4: 1, 5: 2, 6: 4, 7: 7, 8: 11, 9: 17, 10: 25, 11: 36, 12: 50, 13: 70
                             , 14: 94}
    for i in range(320):
        spi = gen.next()
        order = spi.order
        if order not in order_counts.keys():
            order_counts.update({order: 1})
        else:
            order_counts.update({order: order_counts[order] + 1})
    print order_counts
    for order, count in expected_order_counts.iteritems():
        assert order_counts[order] == count
