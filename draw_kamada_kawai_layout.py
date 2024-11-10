import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import collections


class KamadaKawaiLayoutDrawer:
    def __init__(self, graph_data):
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"])
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])
        self.draw_kamada_kawai_layout()

    def draw_kamada_kawai_layout(self):
        fig, ax = plt.subplots(figsize=(8, 8))
        pos = nx.kamada_kawai_layout(self.G)

        # Draw nodes and edges
        nx.draw_networkx_nodes(self.G, pos, node_size=50, node_color="blue", ax=ax)
        nx.draw_networkx_edges(self.G, pos, ax=ax)
        nx.draw_networkx_labels(self.G, pos, font_size=8, font_color="white", ax=ax)
        plt.title("Kamada-Kawai Layout")
        plt.savefig("kamada_kawai_layout.svg", format="svg")
        plt.show()