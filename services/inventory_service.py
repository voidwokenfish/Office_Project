from models import Item, ItemType, RoomType, ItemInventory
from services.repository.exeptions import EmptyFieldException, IdNotFoundException, IdAlreadyInventoriedException
from repository.sqlite_repository import set_inventory_table
from services.repository.sqlite_repository import SqlItemRepository, SqlInventoryRepository
from tests import item_inventory_repo, sql_item_repo
from services.exceptions import *


class ItemInventoryService:
    inventoried_list: list
    total_items: int

    def __init__(self, item_repo: SqlItemRepository, item_inventory_repo: SqlInventoryRepository):
        self.inventoried_list = []
        self.total_items = 0
        self.item_inventory_repo = item_inventory_repo
        self.item_repo = item_repo

    def start_inventory(self, item_type: ItemType = None, room: RoomType = None) -> bool:

        result = sql_item_repo.list(item_type=item_type, room=room)

        set_inventory_table(result)

        self.total_items = len(result)
        return True

    def inventory_item(self, entity: Item) -> bool:
        try:
            item_inventory_repo.update(ItemInventory(entity.id, 1))

            item_inventory_repo.update(entity)
        except EmptyFieldException:
            raise IncorrectItemError
        else:
            return True

    def finish_inventory(self):
        found_items = []
        unfound_items = []
        pass

    def get_inventory_progress(self, entity: ItemInventory) -> bool or str:
        try:
            if entity.id in self.inventoried_list:
                raise IdAlreadyInventoriedException(f"Данный предмет с id {entity.id} уже был инвентаризирован.")

            self.inventoried_list.append(entity.id)
        except IdAlreadyInventoriedException as e:
            return str(e)

        return True



