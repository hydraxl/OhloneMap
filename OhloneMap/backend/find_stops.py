from backend.constants import STOP_TYPES
from backend.access_data import find_nodes

# iterate through path and keep stops
# when encounter stop, ignore until new type is found
def find_stops(path: list[str]) -> list[str]:
    nodes = find_nodes()

    all_stops = []
    last_stop_type = None

    for loc in path:
        if loc == path[-1]:
            all_stops.append(loc)
            break
        
        current_type = nodes[loc]['type']
        if current_type != last_stop_type and current_type in STOP_TYPES:
            last_stop_type = current_type
            all_stops.append(loc)
    
    return all_stops