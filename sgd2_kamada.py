import matplotlib.pyplot as plt
from s_gd2 import sg2
from draw_with_crossings import draw_with_crossings


class SGD2KamadaKawaiLayoutDrawer:
    def __init__(self, graph_data):
        # Prepare graph in a format compatible with s_gd2
        self.graph_data = graph_data
        self.nodes = [node["id"] for node in graph_data["nodes"]]
        self.edges = [(edge["source"], edge["target"]) for edge in graph_data["edges"]]
        self.pos = None  # To store calculated positions
        self.draw_sgd2_kamada_kawai_layout()

    def draw_sgd2_kamada_kawai_layout(self):
        # Convert nodes and edges to the format required by s_gd2
        sg2_graph = sg2.Graph()
        sg2_graph.add_nodes_from(self.nodes)
        sg2_graph.add_edges_from(self.edges)

        # Run the Kamada-Kawai layout algorithm from s_gd2
        self.pos = sg2_graph.layout("kamada-kawai")

        # Convert the positions to a dictionary format for drawing
        pos_dict = {node: (self.pos[node][0], self.pos[node][1]) for node in self.nodes}

        # Visualize and save the layout
        draw_with_crossings(
            sg2_graph,
            pos_dict,
            "SGD2 Kamada-Kawai Layout",
            "sgd2_kamada_kawai_layout.svg",
            "sgd2_kamada"
        )
