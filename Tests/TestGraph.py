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
    assert g0.node_dict == {}
    g0.add_node()
    g0.add_node("test_label")
    g0.add_node()

    assert 0 in g0.node_dict.keys()
    assert 1 in g0.node_dict.keys()
    assert 2 in g0.node_dict.keys()

    assert g0.node_dict[0] is None
    assert g0.node_dict[1] is "test_label"
    assert g0.node_dict[2] is None


def test_add_edge(g3):
    assert g3.edge_list == []
    g3.add_edge(0, 1)
    assert (0, 1) in g3.edge_list
    g3.add_edge(1, 0)
    assert (1, 0) not in g3.edge_list
    g3.add_edge(2, 0)
    assert (0, 2) in g3.edge_list
    assert (2, 0) not in g3.edge_list
    g3.add_edge(2, 2)
    assert (2, 2) not in g3.edge_list
    g3.add_edge(0, 3)
    assert (0, 3) not in g3.edge_list


def test_remove_node(g3):
    g3.add_edge(0, 1)
    g3.add_edge(0, 2)
    g3.add_edge(1, 2)
    assert len(g3.edge_list) == 3

    g3.remove_node(2)
    assert len(g3.edge_list) == 1
    assert (0, 1) in g3.edge_list
    assert len(g3.node_dict) == 2
    assert 2 not in g3.node_dict.keys()


def test_remove_edge(g3):
    g3.add_edge(0, 1)
    g3.add_edge(0, 2)
    g3.add_edge(1, 2)
    assert len(g3.node_dict.keys()) == 3
    assert len(g3.edge_list) == 3
    assert (1, 2) in g3.edge_list

    g3.remove_edge(1, 2)
    assert len(g3.node_dict.keys()) == 3  # (no change)
    assert len(g3.edge_list) == 2
    assert (1, 2) not in g3.edge_list


def test_clear(g3):
    g3.add_edge(0, 1)
    g3.add_edge(0, 2)
    g3.add_edge(1, 2)
    assert g3.node_dict != {}
    assert g3.edge_list != []
    assert g3._id_next != 0

    g3.clear()
    assert g3.node_dict == {}
    assert g3.edge_list == []
    assert g3._id_next == 0

