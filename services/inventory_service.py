
from repository import repository, sqlite_repository
from models import BaseModel, Item, ItemType, RoomType, ItemInventory, Inventory
from services.exeptions import *
from repository.repository import BaseRepository
from pathlib import Path
from repository.sqlite_repository import SqlItemRepository, SqlInventoryRepository, SqlAllInventoriesRepository
from main import item_repo, item_inventory_repo, all_inventories_repo
from repository.exeptions import *
from datetime import datetime

class ItemInventoryService:
    inventoried_list: list
    total_items: int

    def __init__(self, item_repo: SqlItemRepository, item_inventory_repo: SqlInventoryRepository, all_inventories_repo: SqlAllInventoriesRepository):
        self.inventoried_list = []
        self.total_items = 0
        self.item_inventory_repo = item_inventory_repo
        self.item_repo = item_repo
        self.all_inventories_repo = all_inventories_repo

    def start_inventory(self, item_type: ItemType = None, room: RoomType = None) -> bool:

        result = item_repo.list(item_type=item_type, room=room)

        """ЗАПИСЬ О НАЧАЛЕ ИНВЕНТАРИЗАЦИИ"""
        current_date = datetime.now().date
        all_inventories_repo.add(Inventory(current_date, current_date))

        self.total_items = len(result)
        return True

    def inventory_item(self, item_id: int, inventory_id: int) -> bool:

        entity = item_repo.get(item_id)
        inventory = all_inventories_repo.get(inventory_id)
        try:

            item_inventory_repo.add(ItemInventory(item_id=entity.id, inventory_id=inventory.id))

        except EmptyFieldException:

            raise IncorrectItemError

        else:

            return True


    def finish_inventory(self, inventory: Inventory):
        found_items = []
        unfound_items = []
        all_inventories_repo.update(inventory, status="finished")
        return True


    def inventory_progress(self, entity: ItemInventory) -> list:
        pass



    def unfound_ckeck(self):
        all_items = item_repo.list()
        inventoried_items = item_inventory_repo.list()




