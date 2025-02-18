import random
import math
import networkx as nx
import numpy as np
import json
import matplotlib.pyplot as plt
from solve_least_crossing import solve_least_crossings
import networkx as nx
from GridSnapper import apply_grid_snapping
import time


class SimulatedAnnealingDrawer:
    def __init__(self, graph_data, max_iterations=1000, initial_temp=100.0, cooling_rate=0.95,
                 output_file='optimized_graph_layout.json'):
        self.graph_data = graph_data.copy()  # Create a copy to avoid modifying the original
        self.max_iterations = max_iterations
        self.temp = initial_temp
        self.cooling_rate = cooling_rate
        self.width = graph_data["width"]
        self.height = graph_data["height"]
        self.output_file = output_file

        # Generate initial Kamada-Kawai layout
        self._generate_kamada_kawai_layout()

        self.G = nx.Graph()
        self.pos = {}
        self._load_graph()
        self.optimize()
        self.draw("final_graph_layout.svg")
        self._export_to_json()

    def _generate_kamada_kawai_layout(self):
        # Create a temporary graph for Kamada-Kawai layout
        G = nx.Graph()
        for node in self.graph_data["nodes"]:
            G.add_node(node["id"])
        for edge in self.graph_data["edges"]:
            G.add_edge(edge["source"], edge["target"])

        # Compute Kamada-Kawai layout (values in range [-1,1])
        pos = nx.kamada_kawai_layout(G)

        # Map positions from [-1,1] to [0, width] and [0, height]
        for node, (x, y) in pos.items():
            new_x = (x + 1) / 2 * self.width
            new_y = (y + 1) / 2 * self.height

            # Update node positions in graph_data
            for graph_node in self.graph_data["nodes"]:
                if graph_node["id"] == node:
                    graph_node["x"] = new_x
                    graph_node["y"] = new_y
                    break

    def _load_graph(self):
        for node in self.graph_data["nodes"]:
            self.G.add_node(node["id"])
            self.pos[node["id"]] = (node["x"], node["y"])
            self.G.nodes[node["id"]]["pos"] = self.pos[node["id"]]
        for edge in self.graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])

    def _sync_positions_with_graph(self):
        for node, position in self.pos.items():
            self.G.nodes[node]["pos"] = position

    def _move_node_randomly(self, node, radius=10):
        for _ in range(10):  # Try up to 10 times to find a valid position
            x, y = self.pos[node]
            new_x = max(0, min(self.width, x + random.randint(-radius, radius)))
            new_y = max(0, min(self.height, y + random.randint(-radius, radius)))

            # Check if the new position overlaps with another node
            if all(np.sqrt((self.pos[n][0] - new_x) ** 2 + (self.pos[n][1] - new_y) ** 2) > 0.1 for n in self.pos if
                   n != node):
                return new_x, new_y

        # If no valid position found after 10 tries, return the original position
        return x, y

    def _calculate_max_crossings(self, crossings):
        return max(crossings.values())

    import time  # Import time module at the top

    def optimize(self):
        start_time = time.time()  # Start measuring time

        self._sync_positions_with_graph()
        current_pos, current_crossings_dict, _ = solve_least_crossings(self.G, type="optimized")
        current_crossings = self._calculate_max_crossings(current_crossings_dict)

        for iteration in range(self.max_iterations):
            if self.temp <= 0 or current_crossings == 1:  # Stop if crossings reach 1
                print("Early stopping: Crossing count reached 1.")
                break

            self._sync_positions_with_graph()
            new_pos, new_crossings_dict, max_crossing_edge = solve_least_crossings(self.G, type="optimized")
            if not max_crossing_edge:
                break

            new_crossings = self._calculate_max_crossings(new_crossings_dict)

            source, target = max_crossing_edge
            node_to_move = random.choice([source, target])

            original_position = self.pos[node_to_move]
            new_position = self._move_node_randomly(node_to_move)
            self.pos[node_to_move] = new_position

            self._sync_positions_with_graph()

            _, test_crossings_dict, _ = solve_least_crossings(self.G, type="optimized")
            test_crossings = self._calculate_max_crossings(test_crossings_dict)

            if test_crossings < current_crossings or random.random() < math.exp(
                    (current_crossings - test_crossings) / self.temp):
                current_crossings = test_crossings
            else:
                self.pos[node_to_move] = original_position

            self.temp *= self.cooling_rate
            print(f"Iteration {iteration + 1}, Temperature: {self.temp:.2f}, Current Crossings: {current_crossings}")

        for node in self.graph_data["nodes"]:
            node_id = node["id"]
            node["x"], node["y"] = self.pos[node_id]

        end_time = time.time()  # End measuring time
        runtime = end_time - start_time  # Calculate runtime
        print(f"Optimization complete. Total runtime: {runtime:.4f} seconds")

    def _export_to_json(self):
        # Create a copy of the graph data to avoid modifying the original
        export_data = {
            "nodes": [
                {
                    "id": node["id"],
                    "x": int(node["x"]),  # Convert np.int64 → Python int
                    "y": int(node["y"])  # Convert np.int64 → Python int
                }
                for node in self.graph_data["nodes"]
            ],
            "edges": self.graph_data["edges"],
            "width": int(self.width),  # Convert width to standard int
            "height": int(self.height)  # Convert height to standard int
        }

        with open(self.output_file, 'w') as f:
            json.dump(export_data, f, indent=4)

        print(f"Graph layout exported to {self.output_file}")

    def draw(self, filename="simulated_annealing_layout.svg"):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 10))
        plt.grid(True, linestyle='--', linewidth=1, color='black')
        plt.gca().set_axisbelow(True)
        nx.draw(self.G, self.pos, with_labels=True, node_color='blue', node_size=300, font_size=10, font_weight='bold')
        plt.title("Simulated Annealing Optimized Layout")
        plt.tight_layout()
        plt.savefig(filename)
        plt.show()