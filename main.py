
from services.repository.sqlite_repository import SqlInventoryRepository, SqlItemRepository, SqlAllInventoriesRepository
from pathlib import Path
from services.inventory_service import *


db_path = Path('data.db')

item_repo = SqlItemRepository(db_path)
item_inventory_repo = SqlInventoryRepository(db_path)
all_inventories_repo = SqlAllInventoriesRepository(db_path)

inventory_service = ItemInventoryService(item_repo, item_inventory_repo)