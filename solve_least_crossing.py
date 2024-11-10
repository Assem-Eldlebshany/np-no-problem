import networkx as nx
from crossing_utils import calculate_crossings, get_edge_with_most_crossings


def solve_least_crossings(graph):
    # Use stored positions if available, otherwise use spring layout
    pos = nx.get_node_attributes(graph, 'pos')
    if not pos:
        pos = nx.spring_layout(graph, seed=42)

    # Calculate crossings
    crossings = calculate_crossings(graph, pos)

    # Get edge with most crossings
    max_crossing_edge, _ = get_edge_with_most_crossings(crossings)

    return pos, crossings, max_crossing_edge
