import json
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import collections
from crossing_utils import calculate_crossings


class ScalableGraphDrawer:
    def __init__(self, filename):
        try:
            with open(filename, 'r') as file:
                self.graph_data = json.load(file)
            print("File loaded successfully.")
            # Create a NetworkX graph to check planarity
            G = nx.Graph()
            for node in self.graph_data["nodes"]:
                G.add_node(node["id"])
            for edge in self.graph_data["edges"]:
                G.add_edge(edge["source"], edge["target"])
            is_planar, _ = nx.check_planarity(G)
            print(f"Graph is {'planar' if is_planar else 'not planar'}")
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            return
        except json.JSONDecodeError:
            print("Error: JSON format in the file is incorrect.")
            return

        # Initialize each layout drawer
        self.drawers = [
            InitialLayoutDrawer(self.graph_data),
            SpringLayoutDrawer(self.graph_data),
            KamadaKawaiLayoutDrawer(self.graph_data),
            PlanarLayoutDrawer(self.graph_data)
        ]


class BaseLayoutDrawer:
    def draw_graph(self, pos, title, filename):
        fig, ax = plt.subplots(figsize=(8, 8))

        # Calculate crossings and find max crossing edge
        crossings = calculate_crossings(self.G, pos)
        max_crossing_edge = max(crossings, key=crossings.get) if crossings else None
        max_crossings = crossings.get(max_crossing_edge, 0) if max_crossing_edge else 0
        print(f"Maximum crossing number in {title}: {max_crossings}")

        # Draw all edges except max crossing edge in black
        edge_list = list(self.G.edges())
        if max_crossing_edge in edge_list:
            edge_list.remove(max_crossing_edge)

        # Draw regular edges
        nx.draw_networkx_edges(self.G, pos, edgelist=edge_list, ax=ax)

        # Draw max crossing edge in red
        if max_crossing_edge:
            nx.draw_networkx_edges(self.G, pos, edgelist=[max_crossing_edge],
                                   edge_color='red', width=2, ax=ax)

        # Draw nodes and labels
        nx.draw_networkx_nodes(self.G, pos, node_size=50, node_color="blue", ax=ax)
        nx.draw_networkx_labels(self.G, pos, font_size=8, font_color="white", ax=ax)

        plt.title(f"{title} (Max Crossings: {max_crossings})")
        plt.savefig(filename, format="svg")
        plt.show()


class InitialLayoutDrawer(BaseLayoutDrawer):
    def __init__(self, graph_data):
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"], pos=(node["x"], node["y"]))
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])

        pos = {node["id"]: (node["x"], node["y"]) for node in graph_data["nodes"]}
        self.draw_graph(pos, "Initial Layout", "initial_layout.svg")


class SpringLayoutDrawer(BaseLayoutDrawer):
    def __init__(self, graph_data):
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"])
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])

        pos = nx.spring_layout(self.G, scale=2, seed=42)
        self.draw_graph(pos, "Spring Layout", "spring_layout.svg")


class KamadaKawaiLayoutDrawer(BaseLayoutDrawer):
    def __init__(self, graph_data):
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"])
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])

        pos = nx.kamada_kawai_layout(self.G)
        self.draw_graph(pos, "Kamada-Kawai Layout", "kamada_kawai_layout.svg")


class PlanarLayoutDrawer(BaseLayoutDrawer):
    def __init__(self, graph_data):
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"])
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])

        self.is_planar, _ = nx.check_planarity(self.G)
        if self.is_planar:
            pos = nx.planar_layout(self.G)
            self.draw_graph(pos, "Planar Layout", "planar_layout.svg")
        else:
            print("Graph is not planar; skipping planar layout.")


# The rest of the files (crossing_utils.py and solve_least_crossings.py) remain unchanged

if __name__ == "__main__":
    graph_file = "file.json"
    print("Starting ScalableGraphDrawer...")
    ScalableGraphDrawer(graph_file)