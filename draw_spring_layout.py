import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import collections
from crossing_utils import calculate_crossings
from draw_with_crossings import draw_with_crossings
from GridSnapper import apply_grid_snapping



class SpringLayoutDrawer:
    def __init__(self, graph_data):
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"])
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])

        # Store width and height from graph_data (for grid snapping)
        self.width = graph_data.get('width', 10)  # Default width
        self.height = graph_data.get('height', 10)  # Default height

        self.draw_spring_layout()

    def draw_spring_layout(self):
        # Compute the Spring layout
        pos = nx.spring_layout(self.G, scale=2, seed=42)

        # Apply grid snapping to the computed positions
        # pos = apply_grid_snapping(self.G, pos, self.width, self.height)

        # Draw the graph with grid-snapped positions
        draw_with_crossings(self.G, pos, "SpringLayout", "spring_layout.svg", "spring")
        plt.show()

