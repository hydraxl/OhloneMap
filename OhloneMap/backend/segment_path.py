from backend.constants import STOP_TYPES
from backend.access_data import find_nodes

def segment_path(path: list[str]) -> list[list[str]]:
    nodes = find_nodes()
    
    path_segments = []
    current_segment = []
    isFirst = True
    prev_type = None
    for loc in path:
        current_segment.append(loc)
        
        current_type = nodes[loc]['type']
        if current_type != prev_type and current_type in STOP_TYPES and not isFirst:
            prev_type = current_type
            path_segments.append(current_segment)
            current_segment = []
        isFirst = False
    
    if current_segment != []:
        path_segments.append(current_segment)
    
    return path_segments
