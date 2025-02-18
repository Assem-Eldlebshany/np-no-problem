import matplotlib.pyplot as plt
import networkx as nx
from draw_with_crossings import draw_with_crossings
from GridSnapper import apply_grid_snapping


class InitialLayoutDrawer:
    def __init__(self, graph_data):
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"], pos=(node["x"], node["y"]))
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])

        # Store width and height from graph_data (for grid snapping)
        self.width = graph_data.get('width', 10)  # Default width
        self.height = graph_data.get('height', 10)  # Default height

        self.draw_initial_layout(graph_data)

    def draw_initial_layout(self, graph_data):
        pos = {node["id"]: (node["x"], node["y"]) for node in graph_data["nodes"]}

        # Apply grid snapping to the computed positions
        # pos = apply_grid_snapping(self.G, pos, self.width, self.height)

        draw_with_crossings(self.G, pos, "Initial Layout", "initial_layout.svg", "initial")
        plt.show()
