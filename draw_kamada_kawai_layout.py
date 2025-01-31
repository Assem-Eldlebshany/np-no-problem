import matplotlib.pyplot as plt
import networkx as nx
from draw_with_crossings import draw_with_crossings
from GridSnapper import apply_grid_snapping  # Import the grid snapping function


class KamadaKawaiLayoutDrawer:
    def __init__(self, graph_data):
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"])
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])

        # Store width and height from graph_data (for grid snapping)
        self.width = graph_data.get('width', 10)  # Default width
        self.height = graph_data.get('height', 10)  # Default height

        self.draw_kamada_kawai_layout()

    def draw_kamada_kawai_layout(self):
        # Compute the Kamada-Kawai layout (values in range [-1,1])
        pos = nx.kamada_kawai_layout(self.G)

        # Map positions from [-1,1] to [0, width] and [0, height]
        for node, (x, y) in pos.items():
            pos[node] = (
                (x + 1) / 2 * self.width,  # Scale x from [-1,1] to [0, width]
                (y + 1) / 2 * self.height  # Scale y from [-1,1] to [0, height]
            )

        # Apply grid snapping
        pos = apply_grid_snapping(self.G, pos, self.width, self.height)

        # Draw the graph with grid-snapped positions
        draw_with_crossings(self.G, pos, "Kamada-Kawai Grid Snapped Layout", "kamada_kawai_snapped_layout.svg",
                            "kamada")

        plt.show()