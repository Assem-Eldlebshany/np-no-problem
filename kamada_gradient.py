import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from draw_with_crossings import draw_with_crossings
from GridSnapper import apply_grid_snapping
from solve_least_crossing import solve_least_crossings


class GradientLayoutDrawer:
    def __init__(self, graph_data, alpha=1.0, learning_rate=0.01, max_iter=100):
        # Create graph
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"])
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])

        # Store width and height from graph data
        self.width = graph_data.get('width', 10)
        self.height = graph_data.get('height', 10)

        # Generate Kamada-Kawai layout first
        pos = nx.kamada_kawai_layout(self.G)

        # Map Kamada-Kawai layout to graph dimensions
        self.pos = {}
        for node in self.G.nodes():
            x, y = pos[node]
            self.pos[node] = (
                (x + 1) / 2 * self.width,
                (y + 1) / 2 * self.height
            )

        self.alpha = alpha
        self.learning_rate = learning_rate
        self.max_iter = max_iter

        self.optimize_layout()

    def optimize_layout(self):
        # Convert positions to numpy array
        pos_array = np.array([self.pos[node] for node in self.G.nodes()])

        # Adjacency matrix
        adjacency_matrix = nx.adjacency_matrix(self.G)

        for iteration in range(self.max_iter):
            # Compute gradient
            gradient = self.compute_gradient(pos_array, adjacency_matrix)

            # Update positions
            pos_array -= self.learning_rate * gradient

            # Optional: Print objective periodically
            if iteration % 10 == 0:
                obj_val = self.compute_objective(pos_array, adjacency_matrix)
                print(f"Iteration {iteration}, Objective Value: {obj_val}")

        # Update positions
        for i, node in enumerate(self.G.nodes()):
            self.pos[node] = pos_array[i]

        # Apply grid snapping
        self.pos = apply_grid_snapping(self.G, self.pos, self.width, self.height)

        # Draw and analyze crossings
        self.draw_and_analyze_crossings()

    def compute_gradient(self, pos_array, adjacency_matrix):
        n = len(pos_array)
        gradient = np.zeros_like(pos_array)

        # Pairwise differences
        diff = pos_array[:, np.newaxis, :] - pos_array[np.newaxis, :, :]
        dist = np.linalg.norm(diff, axis=2)

        # Prevent division by zero
        dist[dist == 0] = 1e-10

        # Gradient for connected edges
        for u in range(n):
            for v in range(n):
                if adjacency_matrix[u, v]:
                    gradient[u] += diff[u, v] / dist[u, v]

        # Gradient for non-connected edges
        for u in range(n):
            for v in range(u + 1, n):
                if not adjacency_matrix[u, v]:
                    gradient[u] -= self.alpha * diff[u, v] / (dist[u, v] ** 2)
                    gradient[v] += self.alpha * diff[u, v] / (dist[u, v] ** 2)

        return gradient

    def compute_objective(self, pos_array, adjacency_matrix):
        n = len(pos_array)

        # Pairwise differences
        diff = pos_array[:, np.newaxis, :] - pos_array[np.newaxis, :, :]
        dist = np.linalg.norm(diff, axis=2)

        # Prevent log(0)
        dist[dist == 0] = 1e-10

        # Connected edges term
        connected_term = 0
        for u in range(n):
            for v in range(n):
                if adjacency_matrix[u, v]:
                    connected_term += dist[u, v]

        # Non-connected edges term
        non_connected_term = 0
        for u in range(n):
            for v in range(u + 1, n):
                if not adjacency_matrix[u, v]:
                    non_connected_term -= self.alpha * np.log(dist[u, v])

        return connected_term + non_connected_term

    def draw_and_analyze_crossings(self):
        # Prepare position data in the format expected by solve_least_crossings
        pos_for_crossings = {node: list(position) for node, position in self.pos.items()}

        # Plot the graph
        plt.figure(figsize=(10, 10))
        plt.grid(True, linestyle='--', linewidth=1, color='black')
        plt.gca().set_axisbelow(True)

        nx.draw(self.G, self.pos, with_labels=True, node_color='blue',
                node_size=300, font_size=10, font_weight='bold')
        plt.title("Gradient Layout Optimized")
        plt.tight_layout()
        plt.savefig("gradient_layout.png")
        plt.close()

        # Analyze and draw crossings
        draw_with_crossings(self.G, pos_for_crossings,
                            "Gradient Layout Crossings",
                            "gradient_layout_crossings.svg",
                            "gradient")