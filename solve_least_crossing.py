import networkx as nx
from crossing_utils import calculate_crossings, get_edge_with_most_crossings


def solve_least_crossings(graph, type):
    if type == "initial" or type == "optimized":
        pos = nx.get_node_attributes(graph, 'pos')
    if type == "spring":
        pos = nx.spring_layout(graph, seed=42)
    elif type == "kamada":
        pos = nx.kamada_kawai_layout(graph)
    elif type == "planar":
        pos = nx.planar_layout(graph)

    # Calculate crossings
    crossings = calculate_crossings(graph, pos)

    # Get edge with most crossings
    max_crossing_edge, _ = get_edge_with_most_crossings(crossings)

    return pos, crossings, max_crossing_edge
