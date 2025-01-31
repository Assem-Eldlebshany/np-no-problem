import matplotlib.pyplot as plt
import networkx as nx
from solve_least_crossing import solve_least_crossings


def draw_with_crossings(G, pos, title, filename, type, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))

    # Calculate crossings and find edge with most crossings
    _, crossings, max_crossing_edge = solve_least_crossings(G, type)
    for edge, count in crossings.items():
        print(f"Edge {edge} has {count} crossings")

    if max_crossing_edge and crossings:
        # Print the number of crossings for the edge with most crossings
        print(f"Edge {max_crossing_edge} has the most crossings: {crossings[max_crossing_edge]} intersections")

        # Create edge colors list
        edge_colors = ['red' if edge == max_crossing_edge else 'black' for edge in G.edges()]

        # Draw the graph with colored edges
        nx.draw_networkx_nodes(G, pos, node_size=50, node_color="blue", ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, font_color="white", ax=ax)
    else:
        # If no crossings found, draw normally
        nx.draw_networkx_nodes(G, pos, node_size=50, node_color="blue", ax=ax)
        nx.draw_networkx_edges(G, pos, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, font_color="white", ax=ax)

    plt.title(title)
    if ax is None:
        plt.show()
