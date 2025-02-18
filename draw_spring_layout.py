import matplotlib.pyplot as plt
import networkx as nx
import json  # Import JSON to save layout
from matplotlib import collections
from crossing_utils import calculate_crossings
from draw_with_crossings import draw_with_crossings
from GridSnapper import apply_grid_snapping


class SpringLayoutDrawer:
    def __init__(self, graph_data, output_file="spring_layout.json"):
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"])
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])

        # Store width and height from graph_data (for grid snapping)
        self.width = graph_data.get('width', 10)  # Default width
        self.height = graph_data.get('height', 10)  # Default height

        self.output_file = output_file  # File to save layout
        self.draw_spring_layout()

    def draw_spring_layout(self):
        # Compute the Spring layout (positions are in an arbitrary scale)
        pos = nx.spring_layout(self.G, scale=2, seed=42)

        # Normalize positions from range [-1, 1] to [0, width] and [0, height]
        min_x = min(p[0] for p in pos.values())
        max_x = max(p[0] for p in pos.values())
        min_y = min(p[1] for p in pos.values())
        max_y = max(p[1] for p in pos.values())

        for node, (x, y) in pos.items():
            pos[node] = (
                (x - min_x) / (max_x - min_x) * self.width,  # Scale x to [0, width]
                (y - min_y) / (max_y - min_y) * self.height  # Scale y to [0, height]
            )

        # Apply grid snapping
        pos = apply_grid_snapping(self.G, pos, self.width, self.height)

        # Save positions to a JSON file
        self.save_layout(pos)

        # Draw the graph with grid-snapped positions
        draw_with_crossings(self.G, pos, "Spring Layout Grid Snapped", "spring_layout.svg", "spring")

        plt.show()

    def save_layout(self, pos):
        graph_data = {
            "nodes": [{"id": node, "x": int(x), "y": int(y)} for node, (x, y) in pos.items()],
            "edges": [{"source": u, "target": v} for u, v in self.G.edges()],
            "width": self.width,
            "height": self.height
        }

        with open(self.output_file, 'w') as f:
            json.dump(graph_data, f, indent=4)

        print(f"Graph layout saved to {self.output_file}")