from backend.access_data import find_graph, find_node

def find_path(initial: str, end: str, avoid_stairs=False) -> list[str]:
    
    graph = find_graph()

    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    
    while current_node != end:
        visited.add(current_node)

        # temporary try-except to handle missing files
        try:
            destinations = graph[current_node]
        except:
            destinations = {}
        
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            # ignore stairs if needed
            if avoid_stairs and find_node(next_node)['type'] == 'stairs':
                continue

            weight = float(graph[current_node][next_node]) + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return None
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    
    # Reverse path
    path = path[::-1]
    return path