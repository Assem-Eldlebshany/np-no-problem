import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import collections


class PlanarLayoutDrawer:
    def __init__(self, graph_data):
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"])
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])
        self.is_planar, _ = nx.check_planarity(self.G)
        self.draw_planar_layout()

    def draw_planar_layout(self):
        if self.is_planar:
            fig, ax = plt.subplots(figsize=(8, 8))
            pos = nx.planar_layout(self.G)

            # Draw nodes and edges
            nx.draw_networkx_nodes(self.G, pos, node_size=50, node_color="blue", ax=ax)
            nx.draw_networkx_edges(self.G, pos, ax=ax)
            nx.draw_networkx_labels(self.G, pos, font_size=8, font_color="white", ax=ax)
            plt.title("Planar Layout")
            plt.savefig("planar_layout.svg", format="svg")
            plt.show()
        else:
            print("Graph is not planar; skipping planar layout.")