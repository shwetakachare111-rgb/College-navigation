"""Responsive interactive 3D campus scene based on the supplied layout."""
from __future__ import annotations

import math
import tkinter as tk
from pathfinding.graph import CampusGraph


# Route pins are placed at building entrances (not their centres), preventing a
# route from visually cutting through a building.
MAP_POINTS = {
    "main_gate": (50, 88, 0), "reception": (35, 71, 0),
    "admin_block": (35, 62, 0), "corridor_a": (37, 50, 0),
    "library": (18, 42, 0), "stairs": (37, 48, 0), "lift": (39, 48, 0),
    "first_floor_corridor": (37, 47, 10), "computer_lab": (35, 47, 10),
    "physics_lab": (35, 21, 10), "classroom_101": (35, 62, 10),
    "cse_ai": (35, 47, 0), "extc_elec": (35, 34, 0),
    "civil_mech": (35, 21, 0), "workshop": (39, 22, 0),
    "pond": (42, 47, 0), "cycle_stand": (42, 72, 0),
    "canteen": (71, 41, 0), "auditorium": (74, 65, 0), "lawn": (30, 82, 0),
}

# Road-following guides keep the displayed route out of building footprints.
ROUTE_GUIDES = {
    frozenset(("main_gate", "reception")): [(50, 88, 0), (37, 88, 0), (37, 71, 0), (35, 71, 0)],
    frozenset(("reception", "admin_block")): [(35, 71, 0), (35, 62, 0)],
    frozenset(("admin_block", "corridor_a")): [(35, 62, 0), (37, 62, 0), (37, 50, 0)],
    frozenset(("corridor_a", "stairs")): [(37, 50, 0), (37, 48, 0)],
    frozenset(("stairs", "first_floor_corridor")): [(37, 48, 0), (37, 47, 10)],
    frozenset(("lift", "first_floor_corridor")): [(39, 48, 0), (37, 48, 0), (37, 47, 10)],
    frozenset(("first_floor_corridor", "computer_lab")): [(37, 47, 10), (35, 47, 10)],
    frozenset(("corridor_a", "library")): [(37, 50, 0), (18, 50, 0), (18, 42, 0)],
    frozenset(("corridor_a", "pond")): [(37, 50, 0), (40, 50, 0), (42, 47, 0)],
    frozenset(("pond", "cycle_stand")): [(42, 47, 0), (42, 72, 0)],
    frozenset(("cycle_stand", "canteen")): [(42, 72, 0), (67, 72, 0), (67, 41, 0), (71, 41, 0)],
    frozenset(("canteen", "auditorium")): [(71, 41, 0), (70, 41, 0), (70, 65, 0), (74, 65, 0)],
}


class CampusScene(tk.Canvas):
    """A resizable pseudo-3D scene with drag rotation and mouse-wheel zoom."""
    def __init__(self, parent: tk.Misc, graph: CampusGraph, **kwargs: object) -> None:
        super().__init__(parent, bg="#10263d", highlightthickness=0, **kwargs)
        self.graph, self.route = graph, []
        self.angle = -0.18
        self.zoom = 1.0
        self._drag_x = 0
        self.bind("<Configure>", lambda _: self.draw())
        self.bind("<ButtonPress-1>", self._start_drag)
        self.bind("<B1-Motion>", self._drag)
        self.bind("<MouseWheel>", self._wheel)

    def _start_drag(self, event: tk.Event) -> None:
        self._drag_x = event.x

    def _drag(self, event: tk.Event) -> None:
        self.angle += (event.x - self._drag_x) / 260
        self._drag_x = event.x
        self.draw()

    def _wheel(self, event: tk.Event) -> None:
        self.zoom = max(.72, min(1.35, self.zoom * (1.1 if event.delta > 0 else .9)))
        self.draw()

    def _scale(self) -> float:
        return max(3.2, min(self.winfo_width() / 120, self.winfo_height() / 82) * self.zoom)

    def project(self, x: float, y: float, z: float = 0) -> tuple[float, float]:
        scale = self._scale()
        dx, dy = x - 50, y - 50
        rx = dx * math.cos(self.angle) - dy * math.sin(self.angle)
        ry = dx * math.sin(self.angle) + dy * math.cos(self.angle)
        return self.winfo_width() / 2 + rx * scale, self.winfo_height() / 2 + ry * scale * .57 - z * scale * .85

    def _line(self, points: list[tuple[float, float]], color: str, width: float) -> None:
        flat = [coordinate for point in points for coordinate in point]
        self.create_line(*flat, fill=color, width=max(2, int(width * self._scale() / 5)), smooth=True, capstyle=tk.ROUND)

    def _road_network(self) -> None:
        # Roads align with the routes shown on the physical campus board.
        roads = [
            [(13, 91), (13, 12)], [(18, 91), (18, 12)],
            [(18, 91), (52, 91), (70, 91), (85, 91)],
            [(37, 12), (37, 71)], [(67, 13), (67, 88)],
            [(68, 34), (91, 34)], [(70, 42), (70, 89)],
            [(37, 50), (67, 50)], [(37, 71), (67, 71)],
        ]
        for road in roads:
            self._line([self.project(x, y) for x, y in road], "#b8c2cd", 6)
            self._line([self.project(x, y) for x, y in road], "#d9e0e7", 4.5)

    def _building(self, node_id: str, box: tuple[float, float, float, float],
                  height: float, top_color: str, label: str) -> None:
        x1, y1, x2, y2 = box
        base = [self.project(x, y) for x, y in ((x1, y1), (x2, y1), (x2, y2), (x1, y2))]
        top = [self.project(x, y, height) for x, y in ((x1, y1), (x2, y1), (x2, y2), (x1, y2))]
        self.create_polygon(base[1], base[2], top[2], top[1], fill="#741b43", outline="#152b44", width=1)
        self.create_polygon(base[2], base[3], top[3], top[2], fill="#8d214d", outline="#152b44", width=1)
        self.create_polygon(top, fill=top_color, outline="#152b44", width=1)
        cx = sum(point[0] for point in top) / 4
        cy = sum(point[1] for point in top) / 4
        self.create_text(cx, cy, text=label, fill="white", font="{Segoe UI} 8 bold", width=max(60, abs(top[1][0]-top[0][0])*1.3), justify=tk.CENTER)

    def _draw_buildings(self) -> None:
        # Draw far structures first for a natural 3D depth order.
        buildings = [
            ("civil_mech", (22, 13, 34, 21), 11, "#ae255c", "CIVIL & MECH"),
            ("workshop", (39, 13, 48, 22), 10, "#b52b63", "WORKSHOP"),
            ("extc_elec", (22, 27, 34, 34), 9, "#b52b63", "EXTC & ELEC"),
            ("canteen", (72, 35, 81, 41), 8, "#c03c70", "CANTEEN"),
            ("cse_ai", (22, 39, 34, 47), 10, "#b52b63", "CSE & AIDS"),
            ("pond", (42, 33, 65, 60), 1, "#2e9ed8", "POND"),
            ("auditorium", (74, 44, 92, 85), 16, "#a82459", "SWAMI VIVEKANANDA\nAUDITORIUM"),
            ("admin_block", (22, 53, 34, 69), 10, "#b52b63", "MAIN BUILDING"),
            ("cycle_stand", (42, 60, 65, 84), 2, "#ca9224", "PARKING AREA"),
            ("library", (10, 14, 17, 67), 11, "#a82459", "LIBRARY &\nLABORATORY"),
            ("lawn", (10, 75, 30, 89), 1, "#47c85b", "LAWN"),
        ]
        for item in buildings:
            self._building(*item)
        self._building("main_gate", (45, 88, 55, 93), 3, "#e8edf1", "MAIN GATE")

    def _draw_route(self) -> None:
        if not self.route:
            return
        route_coordinates: list[tuple[float, float, float]] = []
        for start, end in zip(self.route, self.route[1:]):
            guide = ROUTE_GUIDES.get(frozenset((start, end)))
            if guide:
                start_position = MAP_POINTS.get(start, (50, 50, 0))
                first_distance = abs(guide[0][0] - start_position[0]) + abs(guide[0][1] - start_position[1])
                last_distance = abs(guide[-1][0] - start_position[0]) + abs(guide[-1][1] - start_position[1])
                if last_distance < first_distance:
                    guide = list(reversed(guide))
                route_coordinates.extend(guide)
            else:
                route_coordinates.extend([MAP_POINTS.get(start, (50, 50, 0)), MAP_POINTS.get(end, (50, 50, 0))])
        if len(self.route) == 1:
            route_coordinates = [MAP_POINTS.get(self.route[0], (50, 50, 0))]
        points = [self.project(*coordinate) for coordinate in route_coordinates]
        # A single bright navigation ribbon remains readable above all buildings.
        self._line(points, "#ffffff", 2.5)
        self._line(points, "#167ee6", 1.45)
        node_points = [self.project(*MAP_POINTS.get(node_id, (50, 50, 0))) for node_id in self.route]
        for index, (node_id, point) in enumerate(zip(self.route, node_points)):
            x, y = point
            if index == 0 or index == len(node_points) - 1:
                fill = "#20b67a" if index == 0 else "#ef5350"
                label = "S" if index == 0 else "D"
                self.create_oval(x-11, y-11, x+11, y+11, fill=fill, outline="white", width=2)
                self.create_text(x, y, text=label, fill="white", font="{Segoe UI} 8 bold")
                pin_label = "START" if index == 0 else "DESTINATION"
                self.create_text(x, y-21, text=pin_label, fill="white", font="{Segoe UI} 8 bold")
            else:
                self.create_oval(x-8, y-8, x+8, y+8, fill="white", outline="#167ee6", width=2)
                self.create_text(x, y, text=str(index + 1), fill="#167ee6", font="{Segoe UI} 8 bold")

    def draw(self) -> None:
        self.delete("all")
        if self.winfo_width() < 30 or self.winfo_height() < 30:
            return
        ground = [self.project(x, y) for x, y in ((2, 2), (98, 2), (98, 98), (2, 98))]
        self.create_polygon(ground, fill="#2d805d", outline="#438e70", width=2)
        self._road_network()
        self._draw_buildings()
        self._draw_route()
        self.create_text(22, 25, anchor="w", text="Drag to rotate  •  Mouse wheel to zoom", fill="#e9f4ff", font="{Segoe UI} 10")

    def zoom_in(self) -> None:
        self.zoom = min(1.35, self.zoom * 1.1)
        self.draw()

    def zoom_out(self) -> None:
        self.zoom = max(.72, self.zoom / 1.1)
        self.draw()

    def reset_camera(self) -> None:
        self.angle, self.zoom = -.18, 1.0
        self.draw()

    def show_route(self, nodes: list[str]) -> None:
        self.route = nodes
        self.draw()

    def clear_route(self) -> None:
        self.route = []
        self.draw()
