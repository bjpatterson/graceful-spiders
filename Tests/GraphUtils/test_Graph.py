"""Tests GraphUtils.Graph"""
import pytest
import GraphUtils.Graph as Graph


@pytest.fixture
def g0():
    return Graph.Graph()


@pytest.fixture
def g3():
    g = Graph.Graph()
    g.add_node()
    g.add_node()
    g.add_node()
    return g


def test_add_node(g0):
    assert g0._node_dict == {}
    g0.add_node()
    g0.add_node("test_label")
    g0.add_node()

    assert 0 in g0._node_dict.keys()
    assert 1 in g0._node_dict.keys()
    assert 2 in g0._node_dict.keys()

    assert g0._node_dict[0] is None
    assert g0._node_dict[1] is "test_label"
    assert g0._node_dict[2] is None


def test_add_edge(g3):
    assert g3._edge_set == set()
    g3.add_edge(0, 1)
    assert (0, 1) in g3._edge_set
    g3.add_edge(1, 0)
    assert (1, 0) not in g3._edge_set
    g3.add_edge(2, 0)
    assert (0, 2) in g3._edge_set
    assert (2, 0) not in g3._edge_set
    g3.add_edge(2, 2)
    assert (2, 2) not in g3._edge_set
    g3.add_edge(0, 3)
    assert (0, 3) not in g3._edge_set


def test_remove_node(g3):
    g3.add_edge(0, 1)
    g3.add_edge(0, 2)
    g3.add_edge(1, 2)
    assert len(g3._edge_set) == 3

    g3.remove_node(2)
    assert len(g3._edge_set) == 1
    assert (0, 1) in g3._edge_set
    assert len(g3._node_dict) == 2
    assert 2 not in g3._node_dict.keys()


def test_remove_edge(g3):
    g3.add_edge(0, 1)
    g3.add_edge(0, 2)
    g3.add_edge(1, 2)
    assert len(g3._node_dict.keys()) == 3
    assert len(g3._edge_set) == 3
    assert (1, 2) in g3._edge_set

    g3.remove_edge(1, 2)
    assert len(g3._node_dict.keys()) == 3  # (no change)
    assert len(g3._edge_set) == 2
    assert (1, 2) not in g3._edge_set


def test_reset(g3):
    g3.add_edge(0, 1)
    g3.add_edge(0, 2)
    g3.add_edge(1, 2)
    assert g3._node_dict != dict()
    assert g3._edge_set != set()
    assert g3._id_next != 0

    g3.reset()
    assert g3._node_dict == dict()
    assert g3._edge_set == set()
    assert g3._id_next == 0


def test_get_nodes(g3):
    assert g3.get_nodes() == [0, 1, 2]


def test_get_node_labels(g0):
    g0.add_node()
    g0.add_node("test_label")
    g0.add_node()
    assert g0.get_node_labels() == {0: None, 1: "test_label", 2: None}


def test_get_edges(g3):
    g3.add_edge(0, 1)
    assert (0, 1) in g3.get_edges()
    assert (1, 0) not in g3.get_edges()
    assert (0, 2) not in g3.get_edges()


def test_has_node(g3):
    assert g3.has_node(0)
    assert g3.has_node(1)
    assert g3.has_node(2)
    assert not g3.has_node(3)

def test_has_edge(g3):
    assert not g3.has_edge(0, 1)
    assert not g3.has_edge(1, 0)
    g3.add_edge(1, 0)
    assert g3.has_edge(0, 1)
    assert g3.has_edge(1, 0)

def test_get_label(g0):
    g0.add_node()
    g0.add_node("test")
    assert g0.get_label(0) is None
    assert g0.get_label(1) is "test"

def test_set_label(g3):
    assert g3.get_label(0) is None
    g3.set_label(0, "something")
    assert g3.get_label(0) is "something"

def test_order(g0, g3):
    assert g0.order == 0
    assert g3.order == 3

def test_get_adjacent_nodes(g3):
    assert len(g3.get_adjacent_nodes(0)) is 0
    g3.add_edge(0, 1)
    g3.add_edge(0, 2)
    assert all(node in g3.get_adjacent_nodes(0) for node in [1, 2])
    assert 0 in g3.get_adjacent_nodes(1)
    assert 0 in g3.get_adjacent_nodes(2)

def test_copy(g3):
    bad_copy = g3
    assert len(g3._node_dict) is len(bad_copy._node_dict)
    bad_copy.add_node()
    assert len(g3._node_dict) is len(bad_copy._node_dict)  # same object reference

    good_copy = g3.copy()
    assert len(g3._node_dict) is len(good_copy._node_dict)
    good_copy.add_node()
    assert len(g3._node_dict) is not len(good_copy._node_dict)  # two different object references
