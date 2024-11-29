from unittest import result

from repository import repository, sqlite_repository
from models import Item, ItemType, RoomType
from repository.repository import BaseItemRepository
import json

class EmptyFieldException(Exception):
    pass

class IdNotFoundException(Exception):
    pass


class ItemInventory:
    def __init__(self, repo: BaseItemRepository):
        self.repo = repo

    def start_inventory(self) -> bool:
        self.repo.set_inventory_table
        return True

    def change_item_condition(self, item_id: int) -> bool or str:
        try:
            self.repo.set_inventory_id_true(item_id)
        except EmptyFieldException:
            return "Пустое поле ввода"
        except IdNotFoundException:
            return f"Данный id - {item_id} не найден"
        else:
            return True

    def finish_inventory(self):
        found_items = []
        unfound_items = []
        pass