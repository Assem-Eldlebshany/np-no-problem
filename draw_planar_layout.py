import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class PlanarLayoutDrawer:
    def __init__(self, graph_data):
        self.G = nx.Graph()
        self.node_positions = {}
        self.grid_width = graph_data.get("width", 25)
        self.grid_height = graph_data.get("height", 25)

        # Add nodes and store their positions
        for node in graph_data["nodes"]:
            self.G.add_node(node["id"])
            self.node_positions[node["id"]] = (node["x"], node["y"])

        # Add edges
        for edge in graph_data["edges"]:
            self.G.add_edge(edge["source"], edge["target"])

        # Check if graph is planar
        self.is_planar, _ = nx.check_planarity(self.G)

        # Draw the planar layout
        self.draw_planar_layout()

    def scale_layout_to_integer_grid(self, pos):
        # Convert positions to numpy array for easier manipulation
        positions = np.array(list(pos.values()))

        # Get current bounds
        min_x, max_x = positions[:, 0].min(), positions[:, 0].max()
        min_y, max_y = positions[:, 1].min(), positions[:, 1].max()

        # Calculate scaling factors to leave margin
        margin = 2  # Leave some space at the edges
        available_width = self.grid_width - 2 * margin
        available_height = self.grid_height - 2 * margin

        # Scale to slightly smaller than grid to ensure rounding doesn't exceed bounds
        x_scale = available_width / (max_x - min_x) if max_x != min_x else 1
        y_scale = available_height / (max_y - min_y) if max_y != min_y else 1

        # Use the smaller scaling factor to maintain aspect ratio
        scale = min(x_scale, y_scale)

        # Scale and round to integers
        scaled_pos = {}
        for node, (x, y) in pos.items():
            # Scale coordinates
            scaled_x = (x - min_x) * scale + margin
            scaled_y = (y - min_y) * scale + margin

            # Round to nearest integer
            int_x = int(round(scaled_x))
            int_y = int(round(scaled_y))

            # Ensure within grid bounds
            int_x = max(0, min(int_x, self.grid_width - 1))
            int_y = max(0, min(int_y, self.grid_height - 1))

            scaled_pos[node] = (int_x, int_y)

        # Handle collisions
        self.resolve_collisions(scaled_pos)

        return scaled_pos

    def resolve_collisions(self, pos):
        """Resolve any cases where multiple nodes got rounded to the same grid point."""
        occupied = {}  # (x,y) -> [nodes]

        # Find all collisions
        for node, (x, y) in pos.items():
            if (x, y) not in occupied:
                occupied[(x, y)] = []
            occupied[(x, y)].append(node)

        # Resolve collisions
        for coord, nodes in occupied.items():
            if len(nodes) > 1:
                # If multiple nodes at same point, spread them to adjacent free spots
                x, y = coord
                offset = 0
                for node in nodes[1:]:  # Skip first node
                    offset += 1
                    # Try adjacent positions in a spiral pattern until a free spot is found
                    for dx, dy in self.spiral_offsets(offset):
                        new_x, new_y = x + dx, y + dy
                        if (0 <= new_x < self.grid_width and
                                0 <= new_y < self.grid_height and
                                (new_x, new_y) not in occupied):
                            pos[node] = (new_x, new_y)
                            occupied[(new_x, new_y)] = [node]
                            break

    def spiral_offsets(self, max_distance):
        """Generate coordinates in a spiral pattern up to max_distance."""
        for d in range(1, max_distance + 1):
            for x in range(-d, d + 1):
                yield (x, -d)
                yield (x, d)
            for y in range(-d + 1, d):
                yield (-d, y)
                yield (d, y)

    def draw_planar_layout(self):
        if self.is_planar:
            print("Graph is planar.")

            # Create figure and axis - now 2x2 grid
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 15))

            # Draw initial graph from input positions
            initial_pos = self.node_positions
            nx.draw_networkx_nodes(self.G, initial_pos, node_size=50, node_color="blue", ax=ax1)
            nx.draw_networkx_edges(self.G, initial_pos, ax=ax1)
            nx.draw_networkx_labels(self.G, initial_pos, font_size=8, font_color="black", ax=ax1)
            ax1.set_title("Initial Graph Layout")

            # Draw NetworkX's planar layout
            pos_original = nx.planar_layout(self.G)
            nx.draw_networkx_nodes(self.G, pos_original, node_size=50, node_color="blue", ax=ax2)
            nx.draw_networkx_edges(self.G, pos_original, ax=ax2)
            nx.draw_networkx_labels(self.G, pos_original, font_size=8, font_color="black", ax=ax2)
            ax2.set_title("NetworkX's Planar Layout")

            # Get planar layout and scale to integer grid
            pos_planar = nx.planar_layout(self.G)
            scaled_pos = self.scale_layout_to_integer_grid(pos_planar)

            # Draw scaled layout
            nx.draw_networkx_nodes(self.G, scaled_pos, node_size=50, node_color="blue", ax=ax3)
            nx.draw_networkx_edges(self.G, scaled_pos, ax=ax3)
            nx.draw_networkx_labels(self.G, scaled_pos, font_size=8, font_color="black", ax=ax3)

            # Add grid to scaled layout plot
            ax3.grid(True, linestyle='--', alpha=0.3)
            ax3.set_xticks(range(self.grid_width))
            ax3.set_yticks(range(self.grid_height))
            ax3.set_title("Modified Planar Layout")
            ax3.set_xlim(-1, self.grid_width)
            ax3.set_ylim(-1, self.grid_height)

            plt.tight_layout()
            plt.show()

            # Print integer coordinates
            print("\nNode Coordinates:")
            for node, pos in scaled_pos.items():
                print(f"Node {node}: {pos}")
        else:
            print("Graph is not planar; skipping planar layout.")

    def _export_to_json(self, scaled_pos):
        # Create a copy of the graph data to avoid modifying the original
        export_data = {
            "nodes": [],
            "edges": self.graph_data["edges"],
            "width": self.grid_width,
            "height": self.grid_height
        }

        # Update node positions with scaled positions
        for node in self.graph_data["nodes"]:
            node_id = node["id"]
            x, y = scaled_pos[node_id]
            export_data["nodes"].append({
                "id": node_id,
                "x": x,
                "y": y
            })

        with open(self.output_file, 'w') as f:
            json.dump(export_data, f, indent=4)
        print(f"Graph layout exported to {self.output_file}")
