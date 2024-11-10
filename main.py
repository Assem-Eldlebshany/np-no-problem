import json
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import collections
from itertools import combinations


class ScalableGraphDrawer:
    def __init__(self, filename):
        # Load the graph data from the JSON file
        with open(filename, 'r') as file:
            self.graph_data = json.load(file)

        # Initialize the graph
        self.G = nx.Graph()

        # Add nodes and edges
        for node in self.graph_data["nodes"]:
            self.G.add_node(node["id"], pos=(node["x"], node["y"]))

        for edge in self.graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])

        # Draw the initial layout and spring layout sequentially
        self.draw_initial_layout()
        self.draw_spring_layout()

    def check_intersect(self, line1, line2):
        """Check if two lines intersect using vector cross product method."""
        (x1, y1), (x2, y2) = line1
        (x3, y3), (x4, y4) = line2

        def ccw(a, b, c):
            """Check if three points make a counterclockwise turn."""
            return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

        return ccw((x1, y1), (x3, y3), (x4, y4)) != ccw((x2, y2), (x3, y3), (x4, y4)) and \
            ccw((x1, y1), (x2, y2), (x3, y3)) != ccw((x1, y1), (x2, y2), (x4, y4))

    def calculate_crossings(self, pos):
        crossings = {}
        edges = list(self.G.edges)

        for i, edge1 in enumerate(edges):
            line1 = (pos[edge1[0]], pos[edge1[1]])
            crossings[edge1] = 0

            for j, edge2 in enumerate(edges):
                if i >= j:
                    continue
                line2 = (pos[edge2[0]], pos[edge2[1]])
                if self.check_intersect(line1, line2):
                    crossings[edge1] += 1
                    crossings[edge2] = crossings.get(edge2, 0) + 1

        return crossings

    def draw_initial_layout(self):
        fig, ax = plt.subplots(figsize=(8, 8))

        # Get positions directly from the JSON file
        pos = {node["id"]: (node["x"], node["y"]) for node in self.graph_data["nodes"]}

        # Calculate crossings
        crossings = self.calculate_crossings(pos)
        max_crossing_edge = max(crossings, key=crossings.get)

        # Draw edges with the edge with the most crossings highlighted
        edge_lines = [((pos[u][0], pos[u][1]), (pos[v][0], pos[v][1])) for u, v in self.G.edges]
        colors = ['yellow' if edge == max_crossing_edge else 'black' for edge in self.G.edges]
        widths = [2 if edge == max_crossing_edge else 0.5 for edge in self.G.edges]

        edge_collection = collections.LineCollection(edge_lines, colors=colors, linewidths=widths)
        ax.add_collection(edge_collection)

        # Draw nodes
        nx.draw_networkx_nodes(self.G, pos, node_size=50, node_color="blue", ax=ax)
        nx.draw_networkx_labels(self.G, pos, font_size=8, font_color="white", ax=ax)

        # Set axis limits based on specified width and height from JSON
        width, height = self.graph_data["width"], self.graph_data["height"]
        ax.set_xlim(-1, width + 1)
        ax.set_ylim(-1, height + 1)

        # Grid and aspect ratio
        ax.grid(True)
        ax.set_aspect('equal', adjustable='datalim')
        plt.title("Initial Layout (Based on JSON Coordinates) with Crossings Highlighted")
        plt.axis("on")

        # Save as SVG
        fig.savefig("initial_layout.svg", format="svg")
        plt.show()

    def draw_spring_layout(self):
        fig, ax = plt.subplots(figsize=(8, 8))

        # Generate positions using spring layout
        pos = nx.spring_layout(self.G, scale=2, seed=42)

        # Calculate crossings
        crossings = self.calculate_crossings(pos)
        max_crossing_edge = max(crossings, key=crossings.get)

        # Draw edges with the edge with the most crossings highlighted
        edge_lines = [((pos[u][0], pos[u][1]), (pos[v][0], pos[v][1])) for u, v in self.G.edges]
        colors = ['red' if edge == max_crossing_edge else 'black' for edge in self.G.edges]
        widths = [2 if edge == max_crossing_edge else 0.5 for edge in self.G.edges]

        edge_collection = collections.LineCollection(edge_lines, colors=colors, linewidths=widths)
        ax.add_collection(edge_collection)

        # Draw nodes
        nx.draw_networkx_nodes(self.G, pos, node_size=50, node_color="blue", ax=ax)
        nx.draw_networkx_labels(self.G, pos, font_size=8, font_color="white", ax=ax)

        # Set axis limits to fit positions
        ax.set_xlim(min(x for x, y in pos.values()) - 1, max(x for x, y in pos.values()) + 1)
        ax.set_ylim(min(y for x, y in pos.values()) - 1, max(y for x, y in pos.values()) + 1)

        # Grid and aspect ratio
        ax.grid(True)
        ax.set_aspect('equal', adjustable='datalim')
        plt.title("Spring Layout (Without Grid Snapping) with Crossings Highlighted")
        plt.axis("on")

        # Save as SVG
        fig.savefig("spring_layout.svg", format="svg")
        plt.show()


# Load and draw the graph from the file
graph_file = "file.json"
ScalableGraphDrawer(graph_file)
