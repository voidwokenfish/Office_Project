class BaseModel:
    pass

class RoomType(BaseModel):
    room_name: str
    description: str
    item_room: int
    def __init__(self, item_room, room_name, description):
        self.item_room = item_room
        self.room_name = room_name
        self.description = description


class ItemType(BaseModel):
    type_name: str
    description: str
    item_type: int
    def __init__(self, item_type, type_name, description):
        self.item_type = item_type
        self.type_name = type_name
        self.description = description


class Item(BaseModel):
    id: int
    name: str
    type: ItemType
    room: RoomType

    def __init__(self, name, type, room, id = None):
        self.name = name
        self.type = type
        self.room = room
        self.id = id

class ItemInventory(BaseModel):
    id: int
    state: int
    items: list
    def __init__(self, id, state = 0):
        self.id = id
        self.state = state

    def __len__(self):
        return len(self.items)