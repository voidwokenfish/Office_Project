
from .models import BaseModel, Item, ItemType, RoomType, ItemInventory, Inventory
from services.exceptions import *
from .repository.exceptions import IdNotFoundException
from .repository.sqlite_repository import SqlItemRepository, SqlInventoryRepository, SqlAllInventoriesRepository, \
    SqlRoomRepository, SqlTypeRepository
from typing import Union
from datetime import datetime


class ItemInventoryService:
    inventoried_list: list
    total_items: int

    def __init__(self, item_repo: SqlItemRepository, room_repo: SqlRoomRepository, type_repo: SqlTypeRepository, item_inventory_repo: SqlInventoryRepository, all_inventories_repo: SqlAllInventoriesRepository):
        self.inventoried_list = []
        self.total_items = 0
        self.item_inventory_repo = item_inventory_repo
        self.item_repo = item_repo
        self.room_repo = room_repo
        self.type_repo = type_repo
        self.all_inventories_repo = all_inventories_repo
        self.inventory_id = None

    def start_inventory(self, item_type: ItemType = None, room: RoomType = None) -> Inventory:

        result = self.item_repo.list(item_type=item_type, room=room)

        """ЗАПИСЬ О НАЧАЛЕ ИНВЕНТАРИЗАЦИИ"""
        current_date = datetime.now().strftime("%d-%m-%Y")
        self.all_inventories_repo.add(Inventory(current_date, current_date))
        current_inventory = self.all_inventories_repo.list()[-1]
        self.inventory_id = current_inventory.id
        inv = self.all_inventories_repo.get(self.inventory_id)

        self.total_items = len(result)
        print(f"Inventory {self.inventory_id} started")
        return inv

    def check_entity(self, entity: Union[ItemInventory, ItemType, RoomType]) -> bool:
        if isinstance(entity, ItemInventory):
            inventory_items = self.item_inventory_repo.list(inventory_id=entity.inventory_id)
            for row in inventory_items:
                if row.item_id == int(entity.item_id) and row.inventory_id == entity.inventory_id:
                    return True

        elif isinstance(entity, ItemType):
            item_types = self.type_repo.list()
            for row in item_types:
                if int(row.item_type) == int(entity.item_type):
                    print(f"Найден тип в check_entity: {entity.item_type}")
                    return True

        elif isinstance(entity, RoomType):
            item_rooms = self.room_repo.list()
            for row in item_rooms:
                if int(row.item_room) == int(entity.item_room):
                    print(f"Найдена комната в check_entity: {entity.item_room}")
                    return True

        return False

    def inventory_item(self, item_id: int) -> tuple or None:
        try:
            entity = self.item_repo.get(item_id)
        except IdNotFoundException as e:
            raise IncorrectItemError(f"Ошибка {e}")


        inventoried_item = ItemInventory(self.inventory_id, item_id)
        if self.check_entity(inventoried_item):
            raise IdAlreadyInventoriedException(f"Предмет с id {inventoried_item.item_id} уже был добавлен")

        self.item_inventory_repo.add(inventoried_item)

        type = self.type_repo.get(entity.type)
        room = self.room_repo.get(entity.room)

        return entity, type, room

    def finish_inventory(self) -> tuple:
        try:
            all_items = self.item_repo.list()

            found_items_ids = [
                row[0]  # item_id
                for row in self.item_inventory_repo.list(inventory_id=self.inventory_id)
            ]

            found_items = []
            for item_id in found_items_ids:
                item = self.item_repo.get(item_id)
                if item is not None:

                    item_type = self.type_repo.get(item.type) if isinstance(item.type, int) else item.type
                    item_room = self.room_repo.get(item.room) if isinstance(item.room, int) else item.room

                    found_items.append({
                        "id": item.id,
                        "name": item.name,
                        "type": item_type.type_name if isinstance(item_type, ItemType) else "Unknown",
                        "room": item_room.room_name if isinstance(item_room, RoomType) else "Unknown",
                    })


            unfound_items = []
            for item in all_items:
                if item.id not in found_items_ids:
                    item = self.item_repo.get(item.id)
                    if item is not None:

                        item_type = self.type_repo.get(item.type) if isinstance(item.type, int) else item.type
                        item_room = self.room_repo.get(item.room) if isinstance(item.room, int) else item.room

                        unfound_items.append({
                            "id": item.id,
                            "name": item.name,
                            "type": item_type.type_name if isinstance(item_type, ItemType) else "Unknown",
                            "room": item_room.room_name if isinstance(item_room, RoomType) else "Unknown",
                        })


            to_be_finished_inv = self.all_inventories_repo.get(self.inventory_id)
            self.all_inventories_repo.update(to_be_finished_inv, status="finished")
            finished_inv = self.all_inventories_repo.get(self.inventory_id)

            return found_items, unfound_items, finished_inv

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()


    def cancel_ongoing_inv(self) -> Inventory:
        to_be_canceled_inv = self.all_inventories_repo.get(self.inventory_id)
        self.all_inventories_repo.update(to_be_canceled_inv, status="canceled")
        canceled_inv = self.all_inventories_repo.get(self.inventory_id)
        return canceled_inv


    def get_all_inv_info(self) -> tuple:
        result = self.all_inventories_repo.list()
        length = len(result)
        return length, result

    def get_entities_info(self, filter: str) -> tuple:

        try:
            if filter == "item":
                result = self.item_repo.list()
            elif filter == "type":
                result = self.type_repo.list()
            elif filter == "room":
                result = self.room_repo.list()
            else:
                raise ValueError("Передан неверный фильтр")
            length = len(result)
            return length, result

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()

    def add_entity(self, filter, *args):

        try:
            if filter == "item":
                name, type, room = args

                if name.strip() == "":
                    raise EmptyFieldError(f"Передано пустое поле")

                item = Item(name, type, room)
                self.item_repo.add(item)
                item.id = self.item_repo.cursor.lastrowid
                print(item.id, item.name, item.type, item.room)
                return item

            elif filter == "type":
                id, name, desc = args

                if id.strip() == "":
                    raise EmptyFieldError(f"Передано пустое поле")
                if name.strip() == "":
                    raise EmptyFieldError(f"Передано пустое поле")
                if desc.strip() == "":
                    raise EmptyFieldError(f"Передано пустое поле")

                type = ItemType(id, name, desc)
                if self.check_entity(type):
                    raise EntityCodeIsUsedException(f"Код {type.item_type} уже используется ")

                self.type_repo.add(type)
                return type

            elif filter == "room":
                id, name, desc = args

                if id.strip() == "":
                    raise EmptyFieldError(f"Передано пустое поле")
                if name.strip() == "":
                    raise EmptyFieldError(f"Передано пустое поле")
                if desc.strip() == "":
                    raise EmptyFieldError(f"Передано пустое поле")

                room = RoomType(id, name, desc)

                if self.check_entity(room):
                    raise EntityCodeIsUsedException(f"Код {room.item_room} уже используется ")

                self.room_repo.add(room)
                return room

            else:
                raise ValueError("Некорректный фильтр")

        except EntityCodeIsUsedException as e:
            return None

        except EmptyFieldError as err:
            print(f"Передано пустое поле {err}")
            return None

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()


