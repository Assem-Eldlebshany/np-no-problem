import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import collections


class InitialLayoutDrawer:
    def __init__(self, graph_data):
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"], pos=(node["x"], node["y"]))
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])
        self.draw_initial_layout(graph_data)

    def draw_initial_layout(self, graph_data):
        fig, ax = plt.subplots(figsize=(8, 8))
        pos = {node["id"]: (node["x"], node["y"]) for node in graph_data["nodes"]}

        # Draw nodes and edges
        nx.draw_networkx_nodes(self.G, pos, node_size=50, node_color="blue", ax=ax)
        nx.draw_networkx_edges(self.G, pos, ax=ax)
        nx.draw_networkx_labels(self.G, pos, font_size=8, font_color="white", ax=ax)

        # Set axis limits
        ax.set_xlim(-1, graph_data["width"] + 1)
        ax.set_ylim(-1, graph_data["height"] + 1)
        plt.title("Initial Layout")
        plt.savefig("initial_layout.svg", format="svg")
        plt.show()