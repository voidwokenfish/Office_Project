from repository.repository import BaseRepository
from repository.sqlite_repository import SqlItemRepository, SqlInventoryRepository, SqlTypeRepository, SqlRoomRepository
from models import *
from pathlib import Path




sql_relative_path = Path("../storage/testbase.db")
sql_abs_path = Path.resolve(sql_relative_path)
sql_item_repo = SqlItemRepository(sql_abs_path)
item_inventory_repo = SqlInventoryRepository(sql_abs_path)