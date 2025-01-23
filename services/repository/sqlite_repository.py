import sqlite3

from typing import List
from pathlib import Path
from services.models import Inventory, RoomType, Item, ItemType, BaseModel, ItemInventory
from services.repository.repository import BaseRepository
from services.repository.exceptions import EmptyFieldException, IdNotFoundException
from datetime import datetime


class SqlItemRepository(BaseRepository):
    """table name - items"""


    def __init__(self, sqldb: Path):
        self.sqldb = sqldb
        self.connection = sqlite3.connect(sqldb)
        self.cursor = self.connection.cursor()


    def get(self, id) -> Item:
        self.cursor.execute("""
        SELECT * FROM items WHERE item_id = ?; 
        """, (id,))
        result = self.cursor.fetchone()

        return Item(result[1],result[2],result[3],result[0])

    def list(self, item_type: ItemType = None, room: RoomType = None) -> List[Item]:
        query = "SELECT * FROM items WHERE 1=1"
        params = []

        if item_type is not None:
            query += " AND item_type = ?"
            params.append(item_type)

        if room is not None:
            query += " AND room = ?"
            params.append(room)

        self.cursor.execute(query, params)
        result = self.cursor.fetchall()
        items = []
        for item in result:
            items.append(Item(item[1], item[2], item[3], item[0]))

        return items

    def add(self, entity: Item) -> bool:
        self.cursor.execute("""
        INSERT INTO items (item_name, item_type, item_room) VALUES (?,?,?)
        """, (object,))
        self.connection.commit()

        return True

    def update(self, entity: Item) -> bool:
        self.cursor.execute("""
        UPDATE items SET item_name = ?, item_type = ?, item_room = ? WHERE item_id = ?
        """, (entity,))
        self.connection.commit()

        return True

    def delete(self, entity: Item) -> bool:
        self.cursor.execute("""
        DELETE FROM items WHERE item_id = ?;
        """, (entity,))
        self.connection.commit()

        return True


class SqlTypeRepository(BaseRepository):
    """table name - item_type_table"""

    def __init__(self, sqldb: Path):
        self.sqldb = sqldb
        self.connection = sqlite3.connect(sqldb)
        self.cursor = self.connection.cursor()


    def get(self, id: int) -> ItemType:
        self.cursor.execute("""
                SELECT * FROM item_type_table WHERE item_type = ?; 
                """, (id,))
        result = self.cursor.fetchone()
        return ItemType(result[0],result[1],result[2])

    def list(self) -> List[ItemType]:
        self.cursor.execute("""
                SELECT * FROM item_type_table
                """)
        result = self.cursor.fetchall()
        list = []
        for item in result:
            list.append(ItemType(item[0],item[1],item[2]))

        return list

    def add(self, entity: ItemType) -> bool:
        self.cursor.execute("""
                INSERT INTO item_type_table (item_type, type_name, type_description) VALUES (?,?,?)
                """, (entity.item_type, entity.type_name, entity.description))
        self.connection.commit()

        return True

    def update(self, entity: ItemType) -> bool:
        self.cursor.execute("""
                UPDATE item_type_table SET item_type = ?, type_name = ?, type_description = ? WHERE item_type = ?
                """, (entity.item_type, entity.type_name, entity.description, entity.item_type))
        self.connection.commit()

        return True

    def delete(self, entity: ItemType) -> bool:
        self.cursor.execute("""
                DELETE FROM item_type_table WHERE item_type = ?;
                """, (entity.item_type))
        self.connection.commit()

        return True

class SqlRoomRepository(BaseRepository):
    """table name - item_room_table"""

    def __init__(self, sqldb: Path):
        self.sqldb = sqldb
        self.connection = sqlite3.connect(sqldb)
        self.cursor = self.connection.cursor()

    def get(self, id: int):
        self.cursor.execute("""
                        SELECT * FROM item_room_table WHERE item_room = ?; 
                        """, (id,))
        result = self.cursor.fetchone()
        return ItemType(result[0], result[1], result[2])

    def list(self) -> List[RoomType]:
        self.cursor.execute("""
                        SELECT * FROM item_room_table
                        """)
        result = self.cursor.fetchall()
        list = []
        for item in result:
            list.append(RoomType(item[0], item[1], item[2]))

        return list

    def add(self, entity: RoomType) -> bool:
        self.cursor.execute("""
                INSERT INTO item_room_table (item_room, room_name, room_description) VALUES (?,?,?)
                """, (entity.item_room, entity.room_name, entity.description))
        self.connection.commit()

        return True

    def update(self, entity: RoomType) -> bool:
        self.cursor.execute("""
                UPDATE item_room_table SET item_room = ?, room_name = ?, room_description = ? WHERE item_room = ?
                """, (entity.item_room, entity.room_name, entity.description, entity.item_room))
        self.connection.commit()

        return True

    def delete(self, entity: RoomType) -> bool:
        self.cursor.execute("""
                DELETE FROM item_room_table WHERE item_room = ?;
                """, (entity.item_room))
        self.connection.commit()

        return True


class SqlInventoryRepository(BaseRepository):
    """table name - inventories_progress_table"""

    def __init__(self, sqldb: Path):
        self.sqldb = sqldb
        self.connection = sqlite3.connect(sqldb)
        self.cursor = self.connection.cursor()

    def get(self, id: int):
        pass

    def list(self, inventory_id: int = None, item_id: int = None) -> List[BaseModel]:
        query = "SELECT * FROM inventories_progress_table WHERE 1=1"
        params = []

        if inventory_id is not None:
            query += " AND inventory_id = ?"
            params.append(inventory_id)

        if item_id is not None:
            query += " AND item_id = ?"
            params.append(item_id)

        self.cursor.execute(query, params)
        result = self.cursor.fetchall()
        items = []
        for item in result:
            items.append(item)

        return items

    def add(self, entity: ItemInventory) -> bool:
        if entity.item_id is None:
            raise IdNotFoundException
        self.cursor.execute("""
    INSERT INTO inventories_progress_table (inventory_id, item_id) VALUES (?, ?)
    """, (entity.inventory_id, entity.item_id))
        self.connection.commit()
        return True

    def update(self, entity: ItemInventory) -> bool: #PEREDELAT
        if entity.item_id is None:
            raise IdNotFoundException
        self.cursor.execute("""
        UPDATE inventories_progress_table SET item_id = ? WHERE item_id = ?;
        """, (entity.item_id, entity.item_id))
        self.connection.commit()

        return True

    def delete(self, entity: BaseModel) -> bool:
        pass


class SqlAllInventoriesRepository(BaseRepository):
    """table name - inventories_table"""

    def __init__(self, sqldb: Path):
        self.sqldb = sqldb
        self.connection = sqlite3.connect(sqldb)
        self.cursor = self.connection.cursor()

    def get(self, id: int):
        self.cursor.execute("""
        SELECT * FROM inventories_table WHERE id = ?
        
        """, (id,))
        result = self.cursor.fetchone()
        return Inventory(result[2], result[3], result[1], result[0]) if result else None

    def list(self) -> List[BaseModel]:
        self.cursor.execute(""" 
        SELECT * FROM inventories_table
        """)
        result = self.cursor.fetchall()
        list = []

        for item in result:
            list.append(Inventory(item[2], item[3], item[1], item[0]))
        return list

    def add(self, entity: Inventory) -> bool:
        self.cursor.execute("""
        INSERT INTO inventories_table (created_at, updated_at) VALUES (?,?)
        """, (entity.created_at, entity.updated_at))
        self.connection.commit()
        return True

    def update(self, entity: Inventory, status: str = None) -> bool:
        query = "UPDATE inventories_table SET updated_at = ?"
        params = [datetime.now()]

        if status is not None:
            query += ", status = ?"
            params.append(status)

        query += " WHERE id = ?"
        params.append(entity.id)


        self.cursor.execute(query, params)
        self.connection.commit()
        return True

    def delete(self, entity: Inventory) -> bool:
        self.cursor.execute("""
        DELETE FROM inventories_table WHERE id = ?
        """, (entity.id,))
        self.connection.commit()
        return True







