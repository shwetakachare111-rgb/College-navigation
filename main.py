"""Start the campus navigation desktop app."""
from pathlib import Path
from pathfinding.graph import CampusGraph
from ui.main_window import NavigatorApp


def main() -> None:
    data = Path(__file__).parent / "data"
    graph = CampusGraph.from_json(data / "nodes.json", data / "edges.json")
    NavigatorApp(graph).mainloop()


if __name__ == "__main__":
    main()
