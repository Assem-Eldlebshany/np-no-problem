import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import collections
from crossing_utils import calculate_crossings
from draw_with_crossings import draw_with_crossings



class SpringLayoutDrawer:
    def __init__(self, graph_data):
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"])
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])
        self.draw_spring_layout()

    def draw_spring_layout(self):
        pos = nx.spring_layout(self.G, scale=2, seed=42)
        draw_with_crossings(self.G, pos, "SpringLayout", "spring_layout.svg", "spring")

