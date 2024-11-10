def check_intersect(line1, line2):

    (x1, y1), (x2, y2) = line1
    (x3, y3), (x4, y4) = line2

    # Convert to vectors
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    # Check if lines share an endpoint
    if (x1, y1) in [(x3, y3), (x4, y4)] or (x2, y2) in [(x3, y3), (x4, y4)]:
        return False

    # Calculate vectors
    v1 = (x2 - x1, y2 - y1)
    v2 = (x4 - x3, y4 - y3)
    v3 = (x3 - x1, y3 - y1)

    # Calculate cross products
    cross1 = det(v1, v2)

    # If lines are parallel
    if cross1 == 0:
        return False

    # Calculate intersection parameters
    t1 = det(v3, v2) / cross1
    t2 = det(v3, v1) / cross1

    # Check if intersection occurs within both line segments
    return 0 <= t1 <= 1 and 0 <= t2 <= 1


def calculate_crossings(graph, pos):
    crossings = {}
    edges = list(graph.edges())

    # Initialize crossings count for each edge
    for edge in edges:
        crossings[edge] = 0

    # Check each pair of edges for intersections
    for i, edge1 in enumerate(edges):
        # Get coordinates for first edge
        start1 = pos[edge1[0]]
        end1 = pos[edge1[1]]
        line1 = (start1, end1)

        for j, edge2 in enumerate(edges[i + 1:], i + 1):
            # Get coordinates for second edge
            start2 = pos[edge2[0]]
            end2 = pos[edge2[1]]
            line2 = (start2, end2)

            # Check if edges share a node
            if edge1[0] in edge2 or edge1[1] in edge2:
                continue

            # Check for intersection
            if check_intersect(line1, line2):
                crossings[edge1] += 1
                crossings[edge2] += 1

    return crossings


def get_edge_with_most_crossings(crossings):
    if not crossings:
        return None, 0

    max_edge = max(crossings.items(), key=lambda x: x[1])
    return max_edge[0], max_edge[1]