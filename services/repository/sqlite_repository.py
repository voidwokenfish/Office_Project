import sqlite3

from typing import List
from pathlib import Path
from services.models import RoomType, Item, ItemType, BaseModel, ItemInventory
from services.repository.repository import BaseRepository
from services.exeptions import EmptyFieldException, IdNotFoundException


class SqlItemRepository(BaseRepository):

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
    def __init__(self, sqldb: Path):
        self.sqldb = sqldb
        self.connection = sqlite3.connect(sqldb)
        self.cursor = self.connection.cursor()

    def get(self, id: int):
        pass

    def list(self) -> List[BaseModel]:
        pass

    def add(self, entity: Item) -> bool:
        self.cursor.execute("""
    INSERT INTO inventory_table (item_id, inventory_state) VALUES (?, ?)
    """, (entity.id, 0))
        self.connection.commit()
        return True

    def update(self, entity: ItemInventory) -> bool:
        if entity.id is None:
            raise EmptyFieldException
        self.cursor.execute("""
                SELECT CASE WHEN EXISTS (SELECT 1 FROM inventory_table WHERE item_id = ?) THEN 1
                ELSE 0
                END AS result
                """, (entity.id,))
        result = self.cursor.fetchone()[0]
        if result is False:
            raise IdNotFoundException

        self.cursor.execute("""
        UPDATE inventory_table SET inventory_state = 1 WHERE item_id = ?;
        """, (entity.id,))
        self.connection.commit()

        return True

    def delete(self, entity: BaseModel) -> bool:
        pass


class Junk:
    def __init__(self):
        pass

    def get_items_by_type(self, type: ItemType) -> List[Item]:
        self.cursor.execute("""
        SELECT * FROM items WHERE item_type = ?;
        """, (type,))
        result = self.cursor.fetchall()
        list = []
        for item in result:
            list.append(Item(item[0],item[1],item[2],item[3]))

        return list

    def get_items_by_room(self, room: RoomType) -> List[Item]:
        self.cursor.execute("""
                SELECT * FROM items WHERE item_type = ?;
                """, (room,))
        result = self.cursor.fetchall()
        list = []
        for item in result:
            list.append(Item(item[0], item[1], item[2], item[3]))

        return list

    def set_inventory_table_old(self) -> bool:
        self.cursor.execute("""
        SELECT item_id FROM items
        """)
        result = self.cursor.fetchall()
        item_ids = [(item_id_tuple[0], 0) for item_id_tuple in result]
        self.cursor.executemany("""
        INSERT INTO inventory_table (item_id, inventory_state) VALUES (?, ?)
        """, item_ids)
        self.connection.commit()

        return True

    def set_inventory_id_true(self, item_id: int) -> bool:
        self.cursor.execute("""
        UPDATE inventory_table SET inventory_state = 1 WHERE item_id = ?
        """, (item_id,))
        self.connection.commit()
        return True

    def add_inventory_history(self, date: str, info: list) -> bool:
        self.cursor.execute("""
        INSERT INTO inventory_history (date, info) VALUES (?, ?)
        """, (date, info))
        self.connection.commit()

        return True

    def id_exists_check(self, item_id: int) -> bool:
        if item_id is None:
            raise EmptyFieldException
        self.cursor.execute("""
        SELECT CASE WHEN EXISTS (SELECT 1 FROM inventory_table WHERE item_id = ?) THEN 1
        ELSE 0
        END AS result
        """, (item_id,))
        result = self.cursor.fetchone()[0]
        if result is False:
            raise IdNotFoundException
        return bool(result)


def set_inventory_table(list: List[Item]) -> bool:
    sqldb = Path("../storage/testbase.db")
    connection = sqlite3.connect(sqldb)
    cursor = connection.cursor()

    data_to_insert = [(item.id, 0) for item in list]

    cursor.executemany("""
        INSERT INTO inventory_table (item_id, inventory_state) VALUES (?, ?)
        """, data_to_insert)

    connection.commit()

    return True


sql_relative_path = Path("../../storage/testbase.db")
sql_abs_path = Path.resolve(sql_relative_path)
sqlrepo = SqlItemRepository(sql_abs_path)
sqlrepo.set_inventory_table()



