import sqlite3
import json
from typing import List
from pathlib import Path
from services.models import RoomType, Item, ItemType
from services.repository.repository import BaseItemRepository
from services.services import EmptyFieldException, IdNotFoundException


class SqlItemRepository(BaseItemRepository):

    def __init__(self, sqldb: Path):
        self.sqldb = sqldb
        self.connection = sqlite3.connect(sqldb)
        self.cursor = self.connection.cursor()


    def get_item(self, id) -> Item:
        self.cursor.execute("""
        SELECT * FROM items WHERE item_id = ?; 
        """, (id,))
        result = self.cursor.fetchone()
        return Item(result[0],result[1],result[2],result[3])

    def get_items(self) -> List[Item]:
        self.cursor.execute("""
        SELECT * FROM items
        """)
        result = self.cursor.fetchall()
        list = []
        for item in result:
            list.append(Item(item[0],item[1],item[2],item[3]))

        return list

    def add_item(self, item_name: str, item_type: int, item_room: int) -> bool:
        self.cursor.execute("""
        INSERT INTO items (item_name, item_type, item_room) VALUES (?,?,?)
        """, (item_name, item_type, item_room,))
        self.connection.commit()

        return True

    def update_item(self, item_id: int, item_name: str, item_type: int, item_room: int) -> bool:
        self.cursor.execute("""
        UPDATE items SET item_name = ?, item_type = ?, item_room = ? WHERE item_id = ?
        """, (item_name, item_type, item_room, item_id))
        self.connection.commit()

        return True

    def delete_item(self, id: int) -> bool:
        self.cursor.execute("""
        DELETE FROM items WHERE item_id = ?;
        """, (id,))
        self.connection.commit()

        return True

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

    def set_inventory_table(self) -> bool:
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




sql_relative_path = Path("../../storage/testbase.db")
sql_abs_path = Path.resolve(sql_relative_path)
sqlrepo = SqlItemRepository(sql_abs_path)
sqlrepo.set_inventory_table()



