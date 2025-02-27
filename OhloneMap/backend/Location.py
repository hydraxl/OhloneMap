class Location:
    # connection format: {"id": "", "distance": "", "image_path": ""}
    def __init__(self, id: str, type: str, level: str, *connections: dict[str : str]):
        self.id = id
        self.type = type
        self.level = level
        self.connections = connections