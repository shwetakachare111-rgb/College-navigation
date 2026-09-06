"""Extract locations from Hindi/English requests without an API."""
from navigation.location_search import MAP_LOCATION_IDS, search_locations
from pathfinding.graph import CampusGraph


def extract_locations(text: str, graph: CampusGraph) -> tuple[str | None, str | None]:
    """Match named places in sentence order; defaults start to Main Gate."""
    normalized = text.lower().replace("-", " ")
    found: list[tuple[int, str]] = []
    for node in graph.nodes.values():
        if node.id not in MAP_LOCATION_IDS:
            continue
        terms = (node.name.lower(), node.id.replace("_", " "), *map(str.lower, node.aliases))
        positions = [normalized.find(term) for term in terms if len(term) > 2 and normalized.find(term) >= 0]
        if positions:
            found.append((min(positions), node.id))
    found.sort()
    ids = []
    for _, node_id in found:
        if node_id not in ids:
            ids.append(node_id)
    if len(ids) >= 2:
        return ids[0], ids[-1]
    if len(ids) == 1:
        return "main_gate", ids[0]
    suggestions = search_locations(graph, normalized, 2, map_labels_only=True)
    return ("main_gate", suggestions[0]) if suggestions else (None, None)
