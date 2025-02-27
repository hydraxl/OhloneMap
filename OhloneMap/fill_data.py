import os

from backend.Location import Location
from backend.access_data import add_location
from backend.constants import STOP_TYPES

'''
add_location(
    PATH,
    Location(
        "", # id
        "", # type
        "", # level
        #{"id": "", "distance": "", "image_name": ""} # Connections, can have any number
    )
)
'''

def find_type(loc: str) -> str:
    last = loc[-1]
    if last == 'e':
        return 'elevator'
    elif last == 'b':
        return 'bathroom'
    elif last == 's':
        return 'stairs'
    elif last == 'o':
        return 'office'
    elif last == 'd':
        return 'doorway'
    else:
        return 'room'

def find_level(loc: str) -> str:
    if loc[1] == 'l':
        return loc[2]
    else:
        return loc[1]

def parse_path_name(path_name: str) -> tuple[str]:
    is_first_word = True
    first = ''
    second = ''
    for c in path_name:
        if c == '&':
            is_first_word = False
            continue
        elif is_first_word:
            first += c
        else:
            second += c
    return first, second

def find_connections(loc, path_names):
    connections = []
    for path_name in path_names:
        in_path = False
        path_ends = parse_path_name(path_name)
        other = ''
        if loc == path_ends[0]:
            other = path_ends[1]
            in_path = True
        elif loc == path_ends[1]:
            other = path_ends[0]
            in_path = True
        
        if in_path:
                connections.append(
                    {"id": other, "distance": 1, "image_name": path_name}
                )
        
    return connections

def is_connected_stop(loc1, loc2):
    if loc1 == loc2:
        return False
    if not find_type(loc1) in STOP_TYPES:
        return False
    if loc1[:2] + loc1[3:] == loc2[:2] + loc2[3:]:
        return True
    return False


location_names = [filename[:len(filename) - 4] for filename in os.listdir('data/locations')]
path_names = [filename[:len(filename) - 4] for filename in os.listdir('data/paths')]

for loc in location_names:
    connections = find_connections(loc, path_names)
    if (find_type(loc) in STOP_TYPES):
        for other in location_names:
            if is_connected_stop(loc, other):
                connections.append(
                    {"id": other, "distance": 1, "image_name": ""}
                )

    add_location(Location(
        loc,
        find_type(loc),
        find_level(loc),
        *connections)
    )
