from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from ai.nlp_parser import extract_locations
from navigation.location_search import MAP_LOCATION_IDS, search_locations
from navigation.route_manager import RouteManager
from pathfinding.graph import CampusGraph
from visualization.scene import CampusScene


class NavigatorApp(tk.Tk):
    def __init__(self, graph: CampusGraph) -> None:
        super().__init__()
        self.graph, self.manager = graph, RouteManager(graph)
        self.title("P. R. Pote Patil College Campus Navigator")
        self.geometry("1450x850")
        self.minsize(1100, 680)
        self._build()

    def _build(self) -> None:
        sidebar = tk.Frame(self, bg="#f4f8fc", width=390)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        view = tk.Frame(self, bg="#10263d")
        view.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        tk.Label(sidebar, text="P. R. Pote Patil College", bg="#f4f8fc", fg="#062b55", font="{Segoe UI} 21 bold").pack(anchor="w", padx=30, pady=(38, 4))
        tk.Label(sidebar, text="Engineering & Management, Amravati\nFind the fastest route anywhere on campus.", bg="#f4f8fc", fg="#537aa5", justify="left", font="{Segoe UI} 11").pack(anchor="w", padx=30, pady=(0, 30))
        names = [node.name for node in graph_nodes(self.graph) if node.id in MAP_LOCATION_IDS]
        self.name_to_id = {node.name: node.id for node in graph_nodes(self.graph)
                           if node.id in MAP_LOCATION_IDS}
        self.start_var = tk.StringVar(value="Main Gate")
        self.goal_var = tk.StringVar(value="CSE & AIDS Building")
        self._selector(sidebar, "1  START LOCATION", self.start_var, names)
        self._selector(sidebar, "2  DESTINATION", self.goal_var, names)
        quick = tk.Frame(sidebar, bg="#f4f8fc")
        quick.pack(fill=tk.X, padx=30, pady=10)
        for label in ("CSE & AIDS Building", "Library & Laboratory", "Canteen"):
            tk.Button(quick, text=label.replace(" & Laboratory", ""), command=lambda x=label: self.goal_var.set(x), bg="#e1ecf8", fg="#123b66", relief="flat", padx=10, pady=10).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        self.accessible = tk.BooleanVar(value=False)
        tk.Button(sidebar, text="FIND OPTIMAL PATH", command=self.find_route, bg="#1976df", fg="white", relief="flat", font="{Segoe UI} 11 bold", pady=16).pack(fill=tk.X, padx=30, pady=12)
        buttons = tk.Frame(sidebar, bg="#f4f8fc")
        buttons.pack(fill=tk.X, padx=30)
        tk.Button(buttons, text="Clear route", command=self.clear, bg="#e1ecf8", relief="flat", pady=12).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        tk.Button(buttons, text="Reset camera", command=self.reset_camera, bg="#e1ecf8", relief="flat", pady=12).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))
        tk.Label(sidebar, text="ASK IN HINDI OR ENGLISH", bg="#f4f8fc", fg="#0758af", font="{Segoe UI} 9 bold").pack(anchor="w", padx=30, pady=(28, 8))
        self.request = tk.Entry(sidebar, font="{Segoe UI} 11", relief="solid", bd=1)
        self.request.insert(0, "Main gate se computer lab jana hai")
        self.request.pack(fill=tk.X, padx=30, ipady=12)
        tk.Button(sidebar, text="Use my request", command=self.use_request, bg="#e1ecf8", fg="#173b62", relief="flat", pady=12).pack(fill=tk.X, padx=30, pady=12)
        # Retained as a non-visible status target for error handling; route details
        # are shown directly on the campus map instead of in a sidebar card.
        self.status = tk.Label(sidebar)
        toolbar = tk.Frame(view, bg="#10263d")
        toolbar.pack(fill=tk.X, padx=18, pady=(12, 0))
        tk.Label(toolbar, text="Interactive campus plan", bg="#10263d", fg="white", font="{Segoe UI} 15 bold").pack(side=tk.LEFT)
        tk.Label(toolbar, text="Blue line = selected route", bg="#10263d", fg="#d7e9f8", font="{Segoe UI} 10").pack(side=tk.RIGHT)
        self.scene = CampusScene(view, self.graph)
        tk.Button(toolbar, text="−", command=self.scene.zoom_out, bg="#274865", fg="white", relief="flat", width=3).pack(side=tk.RIGHT, padx=3)
        tk.Button(toolbar, text="+", command=self.scene.zoom_in, bg="#274865", fg="white", relief="flat", width=3).pack(side=tk.RIGHT, padx=3)
        self.scene.pack(fill=tk.BOTH, expand=True)
        self.after(250, self.find_route)

    def _selector(self, parent: tk.Misc, title: str, variable: tk.StringVar, names: list[str]) -> None:
        tk.Label(parent, text=title, bg="#f4f8fc", fg="#0758af", font="{Segoe UI} 9 bold").pack(anchor="w", padx=30, pady=(0, 9))
        combo = ttk.Combobox(parent, values=names, textvariable=variable, state="normal", font="{Segoe UI} 11")
        combo.pack(fill=tk.X, padx=30, ipady=8, pady=(0, 17))
        combo.bind("<KeyRelease>", lambda event, box=combo: self._suggest(box))

    def _suggest(self, combo: ttk.Combobox) -> None:
        matches = search_locations(self.graph, combo.get(), map_labels_only=True)
        combo["values"] = [self.graph.nodes[node_id].name for node_id in matches]

    def _node_id(self, name: str) -> str | None:
        if name in self.name_to_id:
            return self.name_to_id[name]
        matches = search_locations(self.graph, name, 1, map_labels_only=True)
        return matches[0] if matches else None

    def find_route(self) -> None:
        try:
            start = self._node_id(self.start_var.get())
            goal = self._node_id(self.goal_var.get())
            route = self.manager.route(start, goal, self.accessible.get())
            self.scene.show_route(route.nodes)
            names = [self.graph.nodes[node].name for node in route.nodes
                     if node in MAP_LOCATION_IDS]
            directions = []
            for index, name in enumerate(names):
                if index == 0:
                    directions.append(f"S  Start at {name}")
                elif index == len(names) - 1:
                    directions.append(f"D  Arrive at {name}")
                else:
                    directions.append(f"{index + 1}  Follow the blue line to {name}")
            steps = "\n".join(directions)
            self.status.config(
                text=(f"OPTIMAL ROUTE  •  {route.distance:.0f} m\n\n"
                      f"{steps}"),
                bg="white", fg="#173b62"
            )
        except ValueError as error:
            self.status.config(text=str(error), bg="#fde9e7", fg="#a32d23")

    def use_request(self) -> None:
        start, goal = extract_locations(self.request.get(), self.graph)
        if start and goal:
            self.start_var.set(self.graph.nodes[start].name)
            self.goal_var.set(self.graph.nodes[goal].name)
            self.find_route()
        else:
            self.status.config(text="I could not identify locations. Try 'Main Gate se Library jana hai'.", bg="#fde9e7", fg="#a32d23")

    def clear(self) -> None:
        self.scene.clear_route()
        self.status.config(text="Route cleared.", bg="#e7f4e9", fg="#16714c")

    def reset_camera(self) -> None:
        self.scene.reset_camera()


def graph_nodes(graph: CampusGraph):
    return sorted(graph.nodes.values(), key=lambda node: node.name)
