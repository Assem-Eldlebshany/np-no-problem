import numpy as np
import networkx as nx
from collections import defaultdict
from itertools import product

class GridSnapper:
    def __init__(self, graph, positions, width, height):
        self.G = graph
        self.pos = positions
        self.width = width
        self.height = height
        self.snapped_positions = set()  # Track snapped positions to avoid overlaps
        self.edges = list(self.G.edges())  # Store all edges for edge collision checks

    def snap_to_grid(self):
        # Print initial positions
        print("Initial Positions:")
        for node, pos in self.pos.items():
            print(f"Node {node}: {pos}")

        # Dictionary to store proposed snaps and resolve conflicts
        snap_map = defaultdict(list)

        # Iterate over all nodes to find their closest integer position
        for node, pos in self.pos.items():
            # Compute the nearest integer position
            snapped_pos = tuple(np.round(pos).astype(int))

            # Add this node to the snap_map for the snapped position
            snap_map[snapped_pos].append(node)

        # Counter for snapped nodes
        snapped_nodes_count = 0

        # Resolve conflicts: only snap nodes if the snapped position is unique
        for snapped_pos, nodes in snap_map.items():
            if len(nodes) == 1:  # Only one node wants this position
                node = nodes[0]
                old_pos = self.pos[node]
                if self.is_position_legal(snapped_pos, node):
                    self.pos[node] = np.array(snapped_pos)  # Snap to the integer position
                    self.snapped_positions.add(snapped_pos)  # Mark this position as occupied
                    snapped_nodes_count += 1
                    print(f"SNAPPED Node {node}: {old_pos} -> {self.pos[node]}")
                else:
                    print(f"ILLEGAL POSITION for Node {node}: {snapped_pos} - Resolving conflict.")
                    new_pos = self.find_nearest_available_position(snapped_pos, node)
                    self.pos[node] = new_pos
                    self.snapped_positions.add(tuple(new_pos))  # Mark this position as occupied
                    snapped_nodes_count += 1
                    print(f"RESOLVED Node {node}: {old_pos} -> {new_pos}")
            else:
                print(f"CONFLICT at {snapped_pos}: Nodes {nodes} - Resolving conflicts.")
                for node in nodes:
                    new_pos = self.find_nearest_available_position(snapped_pos, node)
                    old_pos = self.pos[node]
                    self.pos[node] = new_pos
                    self.snapped_positions.add(tuple(new_pos))  # Mark this position as occupied
                    snapped_nodes_count += 1
                    print(f"RESOLVED Node {node}: {old_pos} -> {new_pos}")

        # Print final summary
        print(f"\nGrid Snapping Summary:")
        print(f"Total nodes snapped: {snapped_nodes_count}")

        # Print final positions
        print("\nFinal Positions:")
        for node, pos in self.pos.items():
            print(f"Node {node}: {pos}")

        return self.pos

    def is_position_legal(self, position, node):
        # Check if the position is already occupied
        if position in self.snapped_positions:
            return False

        # Check if the position lies on any edge
        for edge in self.edges:
            u, v = edge
            if u == node or v == node:
                continue  # Skip edges involving the current node
            u_pos = self.pos[u]
            v_pos = self.pos[v]
            if self.point_lies_on_edge(position, u_pos, v_pos):
                return False

        return True

    def point_lies_on_edge(self, point, u_pos, v_pos):
        x, y = point
        x1, y1 = u_pos
        x2, y2 = v_pos

        # Check if the point lies on the line segment between u_pos and v_pos
        cross_product = (y2 - y1) * (x - x1) - (x2 - x1) * (y - y1)
        if abs(cross_product) != 0:
            return False  # Not collinear

        # Check if the point lies within the bounding box of the edge
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        return (x >= min_x) and (x <= max_x) and (y >= min_y) and (y <= max_y)

    def find_nearest_available_position(self, desired_pos, node):
        x, y = desired_pos
        for distance in range(1, max(self.width, self.height)):
            # Generate all positions at the current Manhattan distance
            for dx, dy in product(range(-distance, distance + 1), repeat=2):
                if abs(dx) + abs(dy) == distance:
                    new_pos = (x + dx, y + dy)
                    if self.is_position_legal(new_pos, node):
                        return np.array(new_pos)
        # If no position is found (unlikely), return the desired position
        return np.array(desired_pos)


def apply_grid_snapping(graph, positions, width, height):
    print("\n--- Starting Grid Snapping ---")
    snapper = GridSnapper(graph, positions, width, height)
    return snapper.snap_to_grid()