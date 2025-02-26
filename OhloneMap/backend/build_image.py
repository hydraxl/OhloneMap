from PIL import Image
import io
import base64

from backend.access_data import find_connection_image_file
from backend.access_data import find_location_image_file
from backend.access_data import find_floor_map_file

def pillow_image_to_base64_string(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def base64_string_to_pillow_image(base64_str):
    return Image.open(io.BytesIO(base64.decodebytes(bytes(base64_str, "utf-8"))))

def build_image(path_segment):
    start = path_segment[0]
    end = path_segment[-1]
    connection_files = []
    for i in range(len(path_segment) - 1):
        next_file = find_connection_image_file(path_segment[i], path_segment[i+1])
        connection_files.append(next_file)

    # File locations of relevant images
    ending_filepath_start = find_location_image_file(start)
    ending_filepath_end = find_location_image_file(end)
    floor_map_filepath = find_floor_map_file(start)

    # finds floor and loads floor map
    image = Image.open(floor_map_filepath)

    # finds starting room and highlights it
    overlay = Image.open(ending_filepath_start)
    image.paste(overlay, mask=overlay)

    # finds ending room and highlights it
    overlay = Image.open(ending_filepath_end)
    image.paste(overlay, mask=overlay)

    # finds all path segments and highlights them
    for connection_file in connection_files:
        # finds path segment and highlights it
        overlay = Image.open(connection_file)
        image.paste(overlay, mask=overlay)
    
    # accessible URL of map image
    data_url = 'data:image/jpeg;base64,' + pillow_image_to_base64_string(image)
    return data_url