import sqlite3
from pathlib import Path

sqlpath = Path("storage/testbase.db")

def create_connection():
    conn = sqlite3.connect(sqlpath)
    return conn

def create_tables(conn):
    """Создаем все таблицы"""
    print("Создаем таблицу items")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name VARCHAR NOT NULL,
        item_type INTEGER NOT NULL,
        item_room INTEGER NOT NULL
    )
    """)

    print("Создаем таблицу item_type_table")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS item_type_table (
        item_type INTEGER PRIMARY KEY,
        type_name VARCHAR NOT NULL,
        type_description VARCHAR NOT NULL,
        FOREIGN KEY (item_type) REFERENCES items (item_type) 
    )
    """)

    print("Создаем таблицу item_room_table")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS item_room_table (
        item_room INTEGER PRIMARY KEY,
        room_name VARCHAR NOT NULL,
        room_description VARCHAR NOT NULL,
        FOREIGN KEY (item_room) REFERENCES items (item_room)
    )
    """)

    print("Создаем таблицу inventories_table")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventories_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            status VARCHAR NOT NULL DEFAULT 'in progress',
            created_at VARCHAR NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at VARCHAR NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id) REFERENCES inventories_progress_table (inventory_id)
        )
        """)

    print("Создаем таблицу inventories_progress_table")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventories_progress_table (
        inventory_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        FOREIGN KEY (item_id) REFERENCES items (item_id),
        FOREIGN KEY (inventory_id) REFERENCES inventories_table (id)
    )
    """)


    conn.commit()


def set_data(conn):
    """Наполняем таблицы данными"""
    cursor = conn.cursor()
    print("Наполняем таблицу items")
    cursor.execute("INSERT INTO items (item_name, item_type, item_room) VALUES ('MonitorAcer505', 1, 2)")
    cursor.execute("INSERT INTO items (item_name, item_type, item_room) VALUES ('Chair', 2, 2)")
    cursor.execute("INSERT INTO items (item_name, item_type, item_room) VALUES ('Kettle', 1, 3)")
    cursor.execute("INSERT INTO items (item_name, item_type, item_room) VALUES ('PrinterKyoceraDN540', 1, 2)")
    cursor.execute("INSERT INTO items (item_name, item_type, item_room) VALUES ('GoldenStatue', 3, 1)")
    print("Наполняем таблицу item_type_table")
    cursor.execute("INSERT INTO item_type_table (item_type, type_name, type_description) VALUES (1, 'Electronics', 'Everything that works on electricity!')")
    cursor.execute("INSERT INTO item_type_table (item_type, type_name, type_description) VALUES (2, 'Furniture', 'Tables, chairs, descks etc')")
    cursor.execute("INSERT INTO item_type_table (item_type, type_name, type_description) VALUES (3, 'Miscellaneous', 'All that does not fit into other types')")
    print("Наполняем таблицу item_room_table")
    cursor.execute("INSERT INTO item_room_table (item_room, room_name, room_description) VALUES (1, 'Office of the chief', 'Room where the boss is')")
    cursor.execute("INSERT INTO item_room_table (item_room, room_name, room_description) VALUES (2, 'Office room', 'Room where all the workers are')")
    cursor.execute("INSERT INTO item_room_table (item_room, room_name, room_description) VALUES (3, 'Kitchen', 'A place where we eat')")
    print("Все таблицы успешно наполнены данными")
    conn.commit()

def start_migration():
    """Главная функция для запуска миграций"""
    conn = create_connection()
    create_tables(conn)
    set_data(conn)
    conn.close()

if __name__ == "__main__":
    start_migration()