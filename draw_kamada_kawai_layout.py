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
        # Compute the Kamada-Kawai layout
        pos = nx.kamada_kawai_layout(self.G)

        # Apply grid snapping to the computed positions
        pos = apply_grid_snapping(self.G, pos, self.width, self.height)

        # Draw the graph with grid-snapped positions
        draw_with_crossings(self.G, pos, "Kamada-Kawai Grid Snapped Layout", "kamada_kawai_snapped_layout.svg",
                            "kamada")

        # Optionally visualize it
        plt.figure(figsize=(10, 10))
        plt.grid(True, linestyle='--', linewidth=1, color='black')  # Gridlines
        plt.gca().set_axisbelow(True)  # Grid behind the nodes
        nx.draw(self.G, pos, with_labels=True, node_color='blue', node_size=300, font_size=10, font_weight='bold')
        plt.title("Kamada-Kawai Layout with Grid Snapping")
        plt.tight_layout()
        plt.savefig("kamada_kawai_snapped_layout.png")
        plt.show()