
from repository import repository, sqlite_repository
from models import BaseModel, Item, ItemType, RoomType, ItemInventory
from exeptions import EmptyFieldException, IdNotFoundException, IdAlreadyInventoriedException
from repository.repository import BaseRepository
from pathlib import Path
from repository.sqlite_repository import set_inventory_table
from repository.sqlite_repository import SqlItemRepository
from tests import item_inventory_repo, sql_item_repo

class ItemInventory:
    inventoried_list: list
    total_items: int

    def __init__(self):
        self.inventoried_list = []
        self.total_items = 0

    def start_inventory(self, item_type: ItemType = None, room: RoomType = None) -> bool:

        result = sql_item_repo.list(item_type=item_type, room=room)

        set_inventory_table(result)

        self.total_items = len(result)
        return True

    def item_inventoried(self, entity: BaseModel) -> bool or str:
        try:
            item_inventory_repo.update(entity)
        except EmptyFieldException:
            return "Пустое поле ввода"
        except IdNotFoundException:
            return f"Данный id - {entity} не найден"
        else:
            return True

    def finish_inventory(self):
        found_items = []
        unfound_items = []
        pass

    def inventory_progress(self, entity: ItemInventory) -> bool or str:
        try:
            if entity.id in self.inventoried_list:
                raise IdAlreadyInventoriedException(f"Данный предмет с id {entity.id} уже был инвентаризирован.")

            self.inventoried_list.append(entity.id)
        except IdAlreadyInventoriedException as e:
            return str(e)

        return True



