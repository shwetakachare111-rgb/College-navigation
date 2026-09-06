# 🗺️ Campus Navigation & Shortest Path System

An interactive campus-navigation application that combines the **original campus map**, a **graph-based navigation model**, and a **shortest-path algorithm** to help students and visitors find locations and navigate efficiently across campus.

---

## 📌 Overview

Traditional campus maps are useful for identifying buildings and facilities, but they do not provide interactive route guidance.

The **Campus Navigation & Shortest Path System** adds an interactive navigation layer to the original campus plan. Users can explore the map, select locations, calculate the shortest route between two points, and visually follow the resulting route directly on the campus map.

The original campus map is preserved as the primary visual layer, while navigation information is displayed through an interactive overlay.

---

## 🎯 Objectives

The primary objectives of this project are to:

- Provide an interactive digital campus map.
- Help users locate important campus buildings and facilities.
- Calculate the shortest route between two selected locations.
- Visually display the calculated route on the original campus map.
- Provide zoom, pan, and window-resizing functionality.
- Demonstrate the practical application of graph-based algorithms.
- Create a system that can be extended with additional navigation features.

---

## ❗ Problem Statement

Students, visitors, and other campus users may experience difficulties when:

- Finding unfamiliar buildings or facilities.
- Understanding the best route between two locations.
- Using static campus maps on different screen sizes.
- Determining efficient walking routes.
- Following clear visual directions across campus.

A static map provides information about **where locations are**, but does not dynamically answer **how to get from one location to another**.

---

## 💡 Proposed Solution

The proposed system combines the original campus map with a graph-based shortest-path navigation system.

Campus locations are represented as **nodes**, while walkable connections between locations are represented as **edges**. The system uses these relationships to calculate an efficient route between a selected source and destination.

The calculated route is then displayed as an interactive overlay on the original campus map.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🗺️ Original Campus Map | Preserves the supplied campus layout |
| 🖱️ Interactive Map | Explore and interact with campus locations |
| 🔍 Zoom & Pan | Inspect different areas of the campus |
| 📐 Responsive GUI | Adapts to different window sizes |
| 📍 Location Selection | Select source and destination locations |
| 🧭 Shortest Path | Calculates an efficient route between locations |
| 🛣️ Route Overlay | Displays the calculated route directly on the map |
| 🧩 Graph-Based Navigation | Models campus paths using nodes and edges |

---

## 📍 Supported Campus Locations

The system currently supports important locations represented on the campus plan, including:

- Lawn
- Admin, FY, MBA & MCA Building
- CSE & AI Building
- EXTC & ELEC Building
- Civil & Mech Building
- Workshop
- Library & Laboratory
- Pond
- Cycle Stand
- Swami Vivekanand Auditorium
- Canteen

Additional locations can be added to the navigation graph in future versions.

---

## ⚙️ How It Works

The navigation process follows these steps:

```text
Select Source & Destination
            ↓
       Campus Graph
            ↓
   Shortest Path Algorithm
            ↓
       Calculate Route
            ↓
   Display Route on Map

🛠️ Technology Stack
Category
Technology
Programming Language
Python
GUI Framework
PySide6 / Qt
Navigation
Graph-based pathfinding
Pathfinding
Shortest-path algorithm
Map
Original campus map image
Data
JSON
Environment
Python Virtual Environment
Testing
Python testing framework

📁 Project Structure
college_navigation-github-ready/
│
├── ai/
│   ├── __init__.py
│   ├── llm_client.py
│   └── nlp_parser.py
│
├── data/
│   ├── campus_plan.png
│   ├── campus_plan_display.png
│   ├── edges.json
│   └── nodes.json
│
├── navigation/
│   ├── __init__.py
│   ├── location_search.py
│   └── route_manager.py
│
├── pathfinding/
│   ├── __init__.py
│   ├── astar.py
│   ├── graph.py
│   └── heuristics.py
│
├── tests/
│   ├── test_astar.py
│   └── test_search.py
│
├── ui/
│   ├── __init__.py
│   └── main_window.py
│
├── visualization/
│   ├── __init__.py
│   └── scene.py
│
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

🚀 Installation
1. Clone the Repository
git clone https://github.com/shwetakachare111-rgb/College-navigation.git
Navigate to the project directory:
cd College-navigation
2. Create a Virtual Environment
python -m venv .venv
3. Activate the Virtual Environment
Windows PowerShell
.\.venv\Scripts\Activate.ps1
Windows Command Prompt
.venv\Scripts\activate
macOS / Linux
source .venv/bin/activate

▶️ Run the Application
Start the application using:
python main.py
The interactive campus-navigation interface will launch.

🗺️ Interactive Map
The original campus map is maintained as the primary visual layer.
The application provides an interactive overlay for navigation, allowing users to:
Resize the application window.
Zoom in and out.
Pan across the campus map.
Select source and destination locations.
Calculate routes.
View the calculated route visually.
This approach preserves the familiarity of the original campus layout while adding modern navigation functionality.
🧪 Testing
The project includes automated tests for important navigation and pathfinding functionality.
Tests can be executed using:
python -m pytest
The test suite helps verify:
Shortest-path calculations.
Location-search functionality.
Navigation graph behavior.

🎬 Demonstration
For a project demonstration or competition presentation:
Launch the application.
Display the original campus map.
Demonstrate map zooming.
Demonstrate map panning.
Select a source location.
Select a destination location.
Calculate the shortest route.
Display the highlighted route.
Explain the graph-based navigation approach.

🌟 Advantages
Preserves the actual campus map.
Provides an intuitive interactive interface.
Offers visual route guidance.
Supports flexible map navigation.
Demonstrates practical graph algorithms.
Separates map visualization from navigation logic.
Can be extended with additional locations and features.
Provides a foundation for future intelligent navigation systems.

🔮 Future Scope
The system can be enhanced with several advanced features:
📍 GPS-based live navigation
🎙️ Voice-guided directions
♿ Accessible and wheelchair-friendly routes
⏱️ Estimated walking time
🔀 Multiple route options
🏢 Indoor building navigation
📱 Mobile application support
🌐 Web-based campus navigation
🔄 Real-time campus path updates
🤖 AI-powered natural-language navigation
🚧 Temporary route/road closure support
