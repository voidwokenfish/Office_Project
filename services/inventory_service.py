from .models import BaseModel, Item, ItemType, RoomType, ItemInventory, Inventory
from services.exceptions import *
from .repository.exceptions import IdAlreadyInventoriedException, IdNotFoundException
from .repository.sqlite_repository import SqlItemRepository, SqlInventoryRepository, SqlAllInventoriesRepository
# from main import item_repo, item_inventory_repo, all_inventories_repo
from datetime import datetime
# from repository.repository import BaseRepository
# from repository import repository, sqlite_repository
# from pathlib import Path
# from repository.exceptions import *

class ItemInventoryService:
    inventoried_list: list
    total_items: int

    def __init__(self, item_repo: SqlItemRepository, item_inventory_repo: SqlInventoryRepository, all_inventories_repo: SqlAllInventoriesRepository):
        self.inventoried_list = []
        self.total_items = 0
        self.item_inventory_repo = item_inventory_repo
        self.item_repo = item_repo
        self.all_inventories_repo = all_inventories_repo
        self.inventory_id = None

    def start_inventory(self, item_type: ItemType = None, room: RoomType = None) -> bool:

        result = self.item_repo.list(item_type=item_type, room=room)

        """ЗАПИСЬ О НАЧАЛЕ ИНВЕНТАРИЗАЦИИ"""
        current_date = datetime.now().strftime("%d-%m-%Y")
        self.all_inventories_repo.add(Inventory(current_date, current_date))
        current_inventory = self.all_inventories_repo.list()[-1]
        self.inventory_id = current_inventory.id

        self.total_items = len(result)
        print(f"Inventory {self.inventory_id} started")
        return True

    def is_item_in_inventory(self, item_id: int, inventory_id: int) -> bool:

        inventory_items = self.item_inventory_repo.list(inventory_id=inventory_id)
        for row in inventory_items:
            if row[1] == item_id:
                return True
        return False

    def inventory_item(self, item_id: int, inventory_id: int) -> bool:
        try:
            entity = self.item_repo.get(item_id)
        except IdNotFoundException:
            print(f"Данный id {item_id} не найден.")
            return False

        if self.is_item_in_inventory(item_id, inventory_id):
            print(f"Предмет с id {item_id} уже был добавлен.")
            return False
        try:

            self.item_inventory_repo.add(ItemInventory(item_id=entity.id, inventory_id=self.inventory_id))

        except IdAlreadyInventoriedException:
            print("No")
            return False


        return True

    def finish_inventory(self):

        all_items = self.item_repo.list()

        found_items_ids = [
            row[1]  # item_id
            for row in self.item_inventory_repo.list(inventory_id=self.inventory_id)
        ]

        found_items = [
            {"id": item_id, "name": self.item_repo.get(item_id).name}
            for item_id in found_items_ids
        ]

        unfound_items = [
            {"id": item.id, "name": item.name}
            for item in all_items
            if item.id not in found_items_ids
        ]

        to_be_finished_inv = self.all_inventories_repo.get(self.inventory_id)
        result = self.all_inventories_repo.update(to_be_finished_inv, status="finished")

        print(f"Inventory {self.inventory_id} finished successfully: {result}")
        print(f"Found items: {found_items}")
        print(f"Unfound items: {unfound_items}")

        return found_items, unfound_items




