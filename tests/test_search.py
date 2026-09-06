from pathlib import Path
from navigation.location_search import search_locations
from pathfinding.graph import CampusGraph


def test_partial_case_insensitive_search():
    root = Path(__file__).parents[1]
    campus = CampusGraph.from_json(root / "data/nodes.json", root / "data/edges.json")
    assert search_locations(campus, "COMPUTER")[0] == "computer_lab"
    assert search_locations(campus, "lib")[0] == "library"
