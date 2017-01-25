import pytest
import GraphUtils
import GraphUtils.Graph as Graph
import GraphUtils.Checkers.GracefulChecker as gc

@pytest.fixture
def checker():
    return gc.GracefulChecker()

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


def test_find_graceful_labeling(checker, butterfly, path_10):
    graceful_path = checker.find_graceful_labeling(path_10)
    edge_labels = set(range(10))
    assert type(graceful_path) is GraphUtils.Graph.Graph
    for node1, node2 in graceful_path.get_edges():
        # (will crash if duplicates induced labels are present)
        edge_labels.remove(abs(graceful_path.get_label(node1) - graceful_path.get_label(node2)))

    assert checker.find_graceful_labeling(butterfly) is None


def test_find_labeling_from_partial(checker, path_10):
    """ Tested extensively by recursive calls in `test_find_graceful_labeling` """
    pass
