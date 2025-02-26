import json
from backend.Location import Location

DATAFILE = "data/test_data.json"

# adds a new location to the json file
# connection format: {"id": "", "distance": "", "image_path": ""}
def add_location(location: Location) -> None:
    # important variables
    id = location.id
    type = location.type
    level = location.level
    connections = location.connections

    # Load file
    try:
        with open(DATAFILE, 'r') as file:
            data = json.load(file)
    except:
        data = {}
    
    # Update adjacency
    try:
        adjacency = data['adjacency']
    except:
        data['adjacency'] = {}
        adjacency = data['adjacency']
    
    adjacency[id] = {}
    for loc in adjacency:
        for connection in connections:
            if connection["id"] == loc:
                adjacency[loc][id] =  connection['distance']
                break
    
    for connection in connections:
        adjacency[id][connection["id"]] = connection['distance']

    # Update nodes
    try:
        nodes = data['nodes']
    except:
        data['nodes'] = {}
        nodes = data['nodes']
    
    nodes[id] = {
        'type': type, 
        'level': level
        }

    # Update edges
    try:
        edges = data['edges']
    except:
        data['edges'] = []
        edges = data['edges']
    
    for connection in connections:
        for edge in edges:
            if id in edge["locations"]:
                continue
        
        new_edge = {
            "locations": [connection["id"], id], 
            "length": connection["distance"],
            "image_name": connection["image_name"]
        }
        edges.append(new_edge)
    
    # Write to json file
    with open(DATAFILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# returns an adjacency graph for the entire school
def find_graph():
    try:
        with open(DATAFILE, 'r') as file:
            graph = json.load(file)['adjacency']
        return graph
    except:
        return {}

# returns dictionary of all nodes, with id as key
def find_nodes():
    try:
        with open(DATAFILE, 'r') as file:
            nodes = json.load(file)['nodes']
        return nodes
    except:
        return {}

def find_node(id):
    try:
        return find_nodes[id]
    except:
        raise ValueError(f"No Node with id {id}")

def find_location_image_file(id):
    filepath = f'data/locations/{id}.png'
    return filepath

def find_location_level(id):
    with open(DATAFILE, 'r') as file:
        nodes = json.load(file)['nodes']
    
    filepath = nodes[id]['level']
    return filepath

def find_building_num(id):
    return id[0]

def find_floor_map_file(id):
    level = find_location_level(id)
    building = find_building_num(id)
    return f'data/floor_maps/b{building}l{level}.jpg'

def find_connection_image_file(id1, id2):
    with open(DATAFILE, 'r') as file:
        edges = json.load(file)['edges']

    image_name = ''
    for edge in edges:
        if id1 in edge['locations'] and id2 in edge['locations']:
            image_name = edge['image_name']
            break
    
    if image_name == '':
        raise Exception(f"No connections between {id1} and {id2}")
    
    return f"data/paths/{image_name}.png"
