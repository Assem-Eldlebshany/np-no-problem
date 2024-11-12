import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import collections
from draw_with_crossings import draw_with_crossings


class KamadaKawaiLayoutDrawer:
    def __init__(self, graph_data):
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"])
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])
        self.draw_kamada_kawai_layout(graph_data)

    def draw_kamada_kawai_layout(self, graph_data):
        pos = nx.kamada_kawai_layout(self.G)
        draw_with_crossings(self.G, pos, "Kamada-Kawai Layout", "kamada_kawai_layout.svg", "kamada")
