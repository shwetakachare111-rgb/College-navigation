from pathfinding.astar import find_shortest_path
from pathfinding.graph import CampusGraph, Edge, Node


def graph(edges):
    return CampusGraph([Node("a", "A", 0, 0, 0), Node("b", "B", 1, 0, 0),
                        Node("c", "C", 2, 0, 0), Node("up", "Up", 1, 0, 5, 1)], edges)


def test_simple_path():
    result = find_shortest_path(graph([Edge("a", "b", 1), Edge("b", "c", 1)]), "a", "c")
    assert result.nodes == ["a", "b", "c"]
    assert result.distance == 2


def test_selects_cheapest_of_multiple_paths():
    result = find_shortest_path(graph([Edge("a", "c", 10), Edge("a", "b", 1), Edge("b", "c", 1)]), "a", "c")
    assert result.nodes == ["a", "b", "c"]


def test_unreachable_destination():
    assert find_shortest_path(graph([Edge("a", "b", 1)]), "a", "c") is None


def test_start_equals_goal():
    result = find_shortest_path(graph([]), "a", "a")
    assert result.nodes == ["a"] and result.distance == 0


def test_multifloor_path():
    result = find_shortest_path(graph([Edge("a", "up", 6), Edge("up", "c", 6)]), "a", "c")
    assert result.nodes == ["a", "up", "c"]


def test_disabled_edge_is_avoided():
    result = find_shortest_path(graph([Edge("a", "c", 1, enabled=False), Edge("a", "b", 1), Edge("b", "c", 1)]), "a", "c")
    assert result.nodes == ["a", "b", "c"]


def test_accessible_route_avoids_stairs():
    result = find_shortest_path(graph([Edge("a", "c", 1, accessible=False), Edge("a", "b", 2), Edge("b", "c", 2)]), "a", "c", accessible_only=True)
    assert result.nodes == ["a", "b", "c"]
