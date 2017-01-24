import pytest
import GraphUtils.Graph as Graph
import GraphUtils.Checkers.GracefulChecker as gc

@pytest.fixture
def butterfly():
    graph = Graph.Graph()
    for i in range(5):
        graph.add_node()
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 2)
    graph.add_edge(0, 3)
    graph.add_edge(0, 4)
    graph.add_edge(3, 4)
    return graph


@pytest.fixture
def path_10():
    graph = Graph.Graph()
    for i in range(10):
        graph.add_node()
    for i in range(9):
        graph.add_edge(i, i + 1)
    return graph


def test_find_labeling(butterfly, path_10):
    assert False


def test_find_labeling_from_partial(path_10):
    assert False
