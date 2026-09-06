"""Case-insensitive fuzzy campus location search."""
from difflib import SequenceMatcher
from pathfinding.graph import CampusGraph

# These are the places explicitly labelled on the supplied campus board.
MAP_LOCATION_IDS = frozenset({
    "main_gate", "lawn", "admin_block", "cse_ai", "extc_elec",
    "civil_mech", "workshop", "library", "pond", "cycle_stand",
    "canteen", "auditorium",
})


def search_locations(graph: CampusGraph, query: str, limit: int = 8,
                     map_labels_only: bool = False) -> list[str]:
    query = query.strip().lower()
    if not query:
        return [node.id for node in graph.nodes.values()][:limit]
    scored = []
    nodes = (node for node in graph.nodes.values()
             if not map_labels_only or node.id in MAP_LOCATION_IDS)
    for node in nodes:
        terms = (node.name.lower(), node.id.replace("_", " "), *map(str.lower, node.aliases))
        score = max(SequenceMatcher(None, query, term).ratio() for term in terms)
        if any(query in term for term in terms):
            score += 1
        scored.append((score, node.id))
    return [node_id for score, node_id in sorted(scored, reverse=True) if score >= .34][:limit]
