class ItemType:
    name: str
    description: str
    def __init__(self, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description


class RoomType:
    name: str
    description: str
    def __init__(self, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description


class Item:
    id: int
    name: str
    type: ItemType
    room: RoomType

    def __init__(self, name, type, room):
        self.id = id
        self.name = name
        self.type = type
        self.room = room

