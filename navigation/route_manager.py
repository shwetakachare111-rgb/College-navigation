"""Safe orchestration between UI and pathfinding."""
from pathfinding.astar import Route, find_shortest_path
from pathfinding.graph import CampusGraph


class RouteManager:
    def __init__(self, graph: CampusGraph) -> None:
        self.graph = graph

    def route(self, start: str | None, destination: str | None, accessible: bool) -> Route:
        if not start:
            raise ValueError("Please select a start location.")
        if not destination:
            raise ValueError("Please select a destination.")
        result = find_shortest_path(self.graph, start, destination, accessible)
        if result is None:
            raise ValueError("No route is available between these locations.")
        return result
