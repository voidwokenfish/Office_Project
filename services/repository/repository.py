from abc import ABC, abstractmethod
from typing import List
from services.models import Item,ItemType,RoomType

class BaseRepository(ABC):
    pass

class BaseItemRepository(BaseRepository):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_item(self, id) -> Item:
        pass

    @abstractmethod
    def get_items(self) -> List[Item]:
        pass

    @abstractmethod
    def add_item(self, item):
        pass

    @abstractmethod
    def update_item(self, item):
        pass

    @abstractmethod
    def delete_item(self, item):
        pass

    @abstractmethod
    def get_items_by_type(self, type: ItemType) -> List[Item]:
        pass

    @abstractmethod
    def get_items_by_room(self, room: RoomType) -> List[Item]:
        pass