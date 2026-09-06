"""Data-driven weighted campus graph."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Node:
    id: str
    name: str
    x: float
    y: float
    z: float
    floor: int = 0
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True)
class Edge:
    from_node: str
    to_node: str
    distance: float
    cost: float = 1.0
    accessible: bool = True
    enabled: bool = True

    @property
    def weight(self) -> float:
        return self.distance * self.cost


class CampusGraph:
    def __init__(self, nodes: Iterable[Node], edges: Iterable[Edge]) -> None:
        self.nodes = {node.id: node for node in nodes}
        self._edges: dict[str, list[Edge]] = {node_id: [] for node_id in self.nodes}
        for edge in edges:
            if edge.from_node not in self.nodes or edge.to_node not in self.nodes:
                raise ValueError(f"Edge references unknown node: {edge}")
            self._edges[edge.from_node].append(edge)
            self._edges[edge.to_node].append(
                Edge(edge.to_node, edge.from_node, edge.distance, edge.cost,
                     edge.accessible, edge.enabled)
            )

    @classmethod
    def from_json(cls, nodes_path: Path, edges_path: Path) -> "CampusGraph":
        try:
            raw_nodes = json.loads(nodes_path.read_text(encoding="utf-8"))
            raw_edges = json.loads(edges_path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ValueError(f"Campus data file is missing: {exc.filename}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"Campus data contains invalid JSON: {exc}") from exc
        nodes = [Node(**{**item, "aliases": tuple(item.get("aliases", []))}) for item in raw_nodes]
        edges = [Edge(**item) for item in raw_edges]
        return cls(nodes, edges)

    def neighbors(self, node_id: str, accessible_only: bool = False) -> Iterable[Edge]:
        for edge in self._edges.get(node_id, []):
            if edge.enabled and (not accessible_only or edge.accessible):
                yield edge
