from pathlib import Path
from services.inventory_service import *

db_path = Path('data.db')

item_repo = SqlItemRepository(db_path)
item_inventory_repo = SqlInventoryRepository(db_path)

inventory_service = ItemInventoryService(item_repo, item_inventory_repo)

