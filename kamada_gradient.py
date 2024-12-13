import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from draw_with_crossings import draw_with_crossings


class GradientLayoutDrawer:
    def __init__(self, graph_data, alpha=1.0, learning_rate=0.01, max_iter=100):
        self.G = nx.Graph()
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"], pos=(node["x"], node["y"]))
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])

        # Load initial positions from graph data
        self.pos = {node["id"]: (node["x"], node["y"]) for node in graph_data["nodes"]}
        self.alpha = alpha
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.optimize_layout()

    def apply_repulsion(self, pos_array, min_distance):
        for i, pi in enumerate(pos_array):
            for j, pj in enumerate(pos_array):
                if i >= j:
                    continue  # Only check each pair once

                dist = np.linalg.norm(pi - pj)
                if dist < min_distance:  # If nodes are too close
                    # Apply a repulsion force to push nodes apart
                    repulsion = (min_distance - dist) * (pi - pj) / dist
                    pos_array[i] += repulsion / 2
                    pos_array[j] -= repulsion / 2

        return pos_array

    def optimize_layout(self):
        import os 
        if not os.path.isdir('slideshow'): os.mkdir('slideshow')
        # Flatten the initial positions into a NumPy array
        pos_array = np.array([self.pos[node] for node in self.G.nodes()], dtype=np.float64)

        # Minimum allowed distance between nodes (prevention of overlap)
        min_distance = 0.1  # Adjust this based on your graph size

        for iteration in range(self.max_iter):
            gradient = self.compute_gradient(pos_array)
            gradient_norm = np.linalg.norm(gradient)

            # Update positions using gradient descent
            pos_array -= self.learning_rate * gradient

            # Apply repulsion to avoid node overlap
            # pos_array = self.apply_repulsion(pos_array, min_distance)

            # Debugging: print objective value every few iterations
            if iteration % 10 == 0:
                obj_val = self.compute_objective(pos_array)
                print(f"Iteration {iteration}, Objective Value: {obj_val}, Gradient Norm: {gradient_norm}")

                # Clear the figure before drawing the next iteration
                plt.clf()

                # Draw the graph with updated positions
                nx.draw(self.G, {node: pos_array[i] for i, node in enumerate(self.G.nodes())}, with_labels=True)
                plt.title(f"Iteration {iteration}")
                plt.savefig(f"slideshow/layout_iter_{iteration}.png")

        # Update the node positions back to dictionary format
        for i, node in enumerate(self.G.nodes()):
            self.pos[node] = pos_array[i]

        # Draw the optimized graph
        draw_with_crossings(self.G, self.pos, "Optimized Layout", "optimized_layout.svg", "optimized")


    def compute_gradient(self, pos_array):
        from itertools import combinations
        gradient = np.zeros_like(pos_array, dtype=np.float64)  # Ensure gradient is float
        for u, v in combinations(self.G.nodes(),2):
            pu, pv = pos_array[u], pos_array[v]
            dist = np.linalg.norm(pu - pv)
            if dist == 0:
                continue
            # Gradient of ||pu - pv|| - alpha * log(||pu - pv||)
            if self.G.has_edge(u,v):
                grad_uv = (pu - pv) / dist - (self.alpha / (dist * dist)) * (pu - pv)
            else: grad_uv = - (self.alpha / (dist * dist)) * (pu - pv)
            gradient[u] += grad_uv
            gradient[v] -= grad_uv
        return gradient

    def compute_objective(self, pos_array):
        obj_val = 0
        for u, v in self.G.edges():
            pu, pv = pos_array[u], pos_array[v]
            dist = np.linalg.norm(pu - pv)
            if dist == 0:  # Avoid log(0)
                continue
            obj_val += dist - self.alpha * np.log(dist)
        return obj_val