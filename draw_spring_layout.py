import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import collections


class SpringLayoutDrawer:
    def __init__(self, graph_data):
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"])
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])
        self.draw_spring_layout()

    def draw_spring_layout(self):
        fig, ax = plt.subplots(figsize=(8, 8))
        pos = nx.spring_layout(self.G, scale=2, seed=42)

        # Draw nodes and edges
        nx.draw_networkx_nodes(self.G, pos, node_size=50, node_color="blue", ax=ax)
        nx.draw_networkx_edges(self.G, pos, ax=ax)
        nx.draw_networkx_labels(self.G, pos, font_size=8, font_color="white", ax=ax)
        plt.title("Spring Layout")
        plt.savefig("spring_layout.svg", format="svg")
        plt.show()