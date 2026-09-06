"""Distance functions for A*."""
from math import dist
from .graph import Node


def euclidean_3d(a: Node, b: Node) -> float:
    """Admissible straight-line lower bound through the campus."""
    return dist((a.x, a.y, a.z), (b.x, b.y, b.z))
