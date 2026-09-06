"""Standalone A* implementation."""
from __future__ import annotations

import heapq
from dataclasses import dataclass
from itertools import count
from .graph import CampusGraph
from .heuristics import euclidean_3d


@dataclass(frozen=True)
class Route:
    nodes: list[str]
    distance: float


def find_shortest_path(graph: CampusGraph, start_node: str, goal_node: str,
                       accessible_only: bool = False) -> Route | None:
    """Return the optimal A* route or ``None`` when no route is available."""
    if start_node not in graph.nodes or goal_node not in graph.nodes:
        raise ValueError("Start or destination is not a valid campus location.")
    if start_node == goal_node:
        return Route([start_node], 0.0)
    queue: list[tuple[float, int, str]] = []
    serial = count()
    heapq.heappush(queue, (0.0, next(serial), start_node))
    came_from: dict[str, str] = {}
    g_score = {start_node: 0.0}
    while queue:
        _, _, current = heapq.heappop(queue)
        if current == goal_node:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return Route(path, g_score[goal_node])
        for edge in graph.neighbors(current, accessible_only):
            tentative = g_score[current] + edge.weight
            if tentative < g_score.get(edge.to_node, float("inf")):
                came_from[edge.to_node] = current
                g_score[edge.to_node] = tentative
                f_score = tentative + euclidean_3d(graph.nodes[edge.to_node], graph.nodes[goal_node])
                heapq.heappush(queue, (f_score, next(serial), edge.to_node))
    return None
