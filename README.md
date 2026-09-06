# AI-Based 3D College Navigation System

An interactive desktop navigation system for **P. R. Pote Patil College of Engineering & Management, Amravati**. The application recreates the campus layout as a responsive 3D-style map and calculates one optimal route between locations using the A* algorithm.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-1f6feb)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- Interactive pseudo-3D campus view: drag to rotate and use the mouse wheel or toolbar controls to zoom.
- Responsive layout based on the college campus plan.
- One clear **optimal path** calculated with A*; no duplicate route choices.
- Route stays on campus roads and reaches buildings through road-facing entrances.
- Clear route symbols: green `S` for start, blue numbered checkpoints, and red `D` for destination.
- Case-insensitive fuzzy search for only the landmarks visibly labelled on the map.
- Hindi/English natural-language input, for example: `Main gate se canteen jana hai`.
- Search aliases for common terms such as `parking`, `library`, and `aids`.
- Data-driven campus configuration using JSON files.
- Multi-floor and accessible-edge support retained in the routing layer for future expansion.

## Campus locations

The user-facing selector and search show only labels present on the campus map:

| Location | Location |
| --- | --- |
| Main Gate | Lawn |
| Main Building | CSE & AIDS Building |
| EXTC & ELEC Building | Civil & Mech Building |
| Workshop | Library & Laboratory |
| Pond | Parking Area |
| Canteen | Swami Vivekananda Auditorium |

Internal nodes such as corridors, stairs, and floor connectors are kept hidden from the interface but are used by the routing engine when needed.

## Project structure

```text
college_navigation/
├── ai/                    # Hindi/English location extraction fallback
├── data/
│   ├── nodes.json          # Campus locations and aliases
│   └── edges.json          # Weighted route connections
├── navigation/             # Search and route orchestration
├── pathfinding/            # Graph, 3D heuristic, and A* algorithm
├── ui/                     # Tkinter controls and application window
├── visualization/          # Responsive 3D campus scene and route renderer
├── tests/                  # Pytest tests for the routing engine
├── main.py                 # Application entry point
└── requirements.txt
```

## Requirements

- Python 3.10 or later
- Tkinter (included with the standard Windows Python installer)

## Installation

Clone the repository and open its folder:

```bash
git clone https://github.com/YOUR-USERNAME/college-navigation.git
cd college-navigation
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run Python from the virtual environment directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the application

```bash
python main.py
```

1. Select a **Start Location** and **Destination**.
2. Click **Find Optimal Path**.
3. Follow the blue route line: green `S` is the start, numbered circles are checkpoints, and red `D` is the destination.
4. Drag on the map to rotate it; use the mouse wheel or `+` / `−` controls to zoom.

## A* pathfinding

The routing module is independent from the UI and visualization.

```python
from pathfinding.astar import find_shortest_path

route = find_shortest_path(
    graph,
    start_node="main_gate",
    goal_node="canteen",
)
```

For every node, A* evaluates:

- `g(n)`: accumulated weighted travel cost from the start node.
- `h(n)`: Euclidean distance using the node's 3D coordinates.
- `f(n) = g(n) + h(n)`: estimated total route cost.

Edges can define a distance, a cost multiplier, enabled/disabled status, and accessibility flag. This makes the project ready for future route closures, lift support, and accessibility modes.

## Customize the campus

### Add or edit a location

Edit `data/nodes.json`:

```json
{
  "id": "seminar_hall",
  "name": "Seminar Hall",
  "x": 70,
  "y": 40,
  "z": 0,
  "floor": 0,
  "aliases": ["seminar", "hall"]
}
```

### Add a connection

Edit `data/edges.json`:

```json
{
  "from_node": "canteen",
  "to_node": "seminar_hall",
  "distance": 24,
  "cost": 1.0,
  "accessible": true,
  "enabled": true
}
```

To make a location visible in the map selector, also add its ID to `MAP_LOCATION_IDS` in `navigation/location_search.py`. To place it on the 3D map, add an entrance coordinate to `MAP_POINTS` and a building definition in `visualization/scene.py`.

## Natural-language input

The app works without an API through aliases and fuzzy matching. It recognizes straightforward Hindi and English requests such as:

```text
Main gate se canteen jana hai
Library ka rasta batao
Mujhe parking area jana hai
```

`.env.example` reserves `OPENAI_API_KEY` for a future cloud-NLP enhancement. Never commit a real API key.

## Testing

Run the automated tests:

```bash
python -m pytest -q
```

The test suite covers simple routing, shortest-path selection, unreachable locations, same-node routing, multi-floor edges, disabled edges, accessible routes, and fuzzy search.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| `python` is not recognized | Install Python from [python.org](https://www.python.org/downloads/) and select **Add Python to PATH** during installation. |
| PowerShell blocks `Activate.ps1` | Use `.\.venv\Scripts\python.exe main.py` instead of activating the environment. |
| Tkinter window does not open on Linux | Install the system package commonly named `python3-tk`. |
| No route is shown | Check that both selected locations have valid enabled edges in `data/edges.json`. |

## Future improvements

- Indoor floor plans and room-level navigation
- Live route closures and blocked-path controls
- Voice input and API-backed natural language understanding
- Turn-by-turn directions with estimated walking time
- Web and mobile front ends using the same routing module

## License

This project is available under the [MIT License](LICENSE). Add a `LICENSE` file before publishing if one is not already present.
