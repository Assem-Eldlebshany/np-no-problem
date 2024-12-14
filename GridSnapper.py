import numpy as np
import networkx as nx


class GridSnapper:
    def __init__(self, graph, positions, width, height):
        """
        Initialize the GridSnapper with the graph, current positions, and graph dimensions.

        :param graph: NetworkX graph
        :param positions: Dictionary of node positions
        :param width: Width of the graph layout (max x-coordinate)
        :param height: Height of the graph layout (max y-coordinate)
        """
        self.G = graph
        self.pos = positions
        self.width = width
        self.height = height

    def snap_to_grid(self, snap_radius=0.5):
        """
        Snap nodes to integer grid coordinates.

        :param snap_radius: Radius around grid point to search for nodes (default 0.5).
        :return: Updated positions dictionary.
        """
        # Print initial positions
        print("Initial Positions:")
        for node, pos in self.pos.items():
            print(f"Node {node}: {pos}")

        # Convert current positions to numpy array for easier manipulation
        pos_array = np.array(list(self.pos.values()))

        print(f"\nGrid Bounds:")
        print(f"Width: 0 to {self.width}, Height: 0 to {self.height}")
        print(f"Snap Radius: {snap_radius}")

        # Counter for snapped nodes
        snapped_nodes_count = 0

        # Iterate over all integer grid points within the specified width and height
        for x in range(self.width + 1):
            for y in range(self.height + 1):
                # Define the search region around the grid point (x, y)
                region_min = np.array([x - snap_radius, y - snap_radius])
                region_max = np.array([x + snap_radius, y + snap_radius])

                # Find nodes within this region
                nodes_in_region = [
                    node for node, pos in self.pos.items()
                    if np.all(pos >= region_min) and np.all(pos <= region_max)
                ]

                # Debugging for each grid point
                if nodes_in_region:
                    print(f"\nGrid Point ({x}, {y}):")
                    print(f"Region: Min {region_min}, Max {region_max}")
                    print(f"Nodes in region: {nodes_in_region}")

                # Snap to the grid point if exactly one node is found
                if len(nodes_in_region) == 1:
                    node = nodes_in_region[0]
                    old_pos = self.pos[node]
                    self.pos[node] = np.array([x, y])
                    snapped_nodes_count += 1
                    print(f"SNAPPED Node {node}: {old_pos} -> {self.pos[node]}")

        # Print final summary
        print(f"\nGrid Snapping Summary:")
        print(f"Total nodes snapped: {snapped_nodes_count}")

        # Print final positions
        print("\nFinal Positions:")
        for node, pos in self.pos.items():
            print(f"Node {node}: {pos}")

        return self.pos


def apply_grid_snapping(graph, positions, width, height, snap_radius=0.5):
    """
    Convenience function to apply grid snapping.

    :param graph: NetworkX graph
    :param positions: Dictionary of node positions
    :param width: Width of the graph layout (max x-coordinate)
    :param height: Height of the graph layout (max y-coordinate)
    :param snap_radius: Radius around grid point to search for nodes
    :return: Updated positions
    """
    print("\n--- Starting Grid Snapping ---")
    snapper = GridSnapper(graph, positions, width, height)
    return snapper.snap_to_grid(snap_radius)