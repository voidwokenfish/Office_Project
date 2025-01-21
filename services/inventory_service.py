from .models import BaseModel, Item, ItemType, RoomType, ItemInventory, Inventory
from services.exceptions import *
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
        self.unfound_items = []
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
        self.inventory_id = self.all_inventories_repo.list()[-1]

        self.total_items = len(result)
        return True

    def inventory_item(self, item_id: int, inventory_id: int) -> bool:

        entity = self.item_repo.get(item_id)
        inventory = self.all_inventories_repo.get(inventory_id)
        try:

            self.item_inventory_repo.add(ItemInventory(item_id=entity.id, inventory_id=inventory.id))

        except ValueError:

            raise IncorrectItemError

        else:
            self.inventoried_list.append(entity)
            return True


    def finish_inventory(self):
        # found_items = []
        # unfound_items = []

        self.all_inventories_repo.update(self.inventory_id, status="finished")

        print(f"Найдено - {len(self.inventoried_list)}\nНе найдено - {len(self.unfound_items)}\nСписок найденных - {[i[0] for i in self.inventoried_list]}")
        return True


    def inventory_progress(self, entity: ItemInventory) -> list:
        pass



    def unfound_ckeck(self):
        all_items = self.item_repo.list()
        inventoried_items = self.item_inventory_repo.list()




