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
    item_id: int
    inventory_id: int
    def __init__(self, inventory_id, item_id):
        self.inventory_id = inventory_id
        self.item_id = item_id


class Inventory(BaseModel):
    id: int
    status: str
    created_at: str
    updated_at: str
    def __init__(self,created_at, updated_at, status = "in progress", id = None):
        self.id = id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
