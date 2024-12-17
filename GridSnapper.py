import numpy as np
import networkx as nx
from collections import defaultdict


class GridSnapper:
    def __init__(self, graph, positions, width, height):
        self.G = graph
        self.pos = positions
        self.width = width
        self.height = height

    def snap_to_grid(self):
        """
        Snap nodes to the nearest integer grid point.
        If two or more nodes want the same position, none of them are snapped.
        :return: Updated positions dictionary
        """
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
                self.pos[node] = np.array(snapped_pos)  # Snap to the integer position
                snapped_nodes_count += 1
                print(f"SNAPPED Node {node}: {old_pos} -> {self.pos[node]}")
            else:
                print(f"CONFLICT at {snapped_pos}: Nodes {nodes} - None snapped.")

        # Print final summary
        print(f"\nGrid Snapping Summary:")
        print(f"Total nodes snapped: {snapped_nodes_count}")

        # Print final positions
        print("\nFinal Positions:")
        for node, pos in self.pos.items():
            print(f"Node {node}: {pos}")

        return self.pos


def apply_grid_snapping(graph, positions, width, height):
    """
    Apply the optimized grid snapping logic to the given graph and positions.
    :param graph: NetworkX graph
    :param positions: Dictionary of node positions
    :param width: Width of the graph layout
    :param height: Height of the graph layout
    :return: Updated positions
    """
    print("\n--- Starting Grid Snapping ---")
    snapper = GridSnapper(graph, positions, width, height)
    return snapper.snap_to_grid()