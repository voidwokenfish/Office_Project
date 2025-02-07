
from services.repository.sqlite_repository import SqlInventoryRepository, SqlItemRepository, \
    SqlAllInventoriesRepository, SqlRoomRepository, SqlTypeRepository
from pathlib import Path
from services.inventory_service import ItemInventoryService
from exceptions import IncorrectTypeError
from interface.interface import *
import sys






# if __name__ == '__main__':
#     db_path = Path('storage/testbase.db')
#
#     item_repo = SqlItemRepository(db_path)
#     item_inventory_repo = SqlInventoryRepository(db_path)
#     all_inventories_repo = SqlAllInventoriesRepository(db_path)
#
#     inventory_service = ItemInventoryService(item_repo, item_inventory_repo, all_inventories_repo)
#
#
#     while True:
#         user_choice = input(f"Start? 1 = full, 2 = no ")
#         if user_choice == "1":
#             """Проведение полной инвентаризации"""
#             print("Starting full inventory")
#             inventory_service.start_inventory()
#             while True:
#                 item_id = int(input("Enter item's id (0 for end): "))
#                 if item_id == 0:
#                     break
#                 item_instance = item_repo.get(item_id)
#                 if item_instance:
#                     inventory_service.inventory_item(item_instance.id, inventory_service.inventory_id)
#                 else:
#
#                     print("incorrect id")
#                     continue
#             inventory_service.finish_inventory()



if __name__ == '__main__':
    db_path = Path('storage/testbase.db')


    room_repo = SqlRoomRepository(db_path)
    type_repo = SqlTypeRepository(db_path)
    item_repo = SqlItemRepository(db_path)
    item_inventory_repo = SqlInventoryRepository(db_path)
    all_inventories_repo = SqlAllInventoriesRepository(db_path)
    inventory_service = ItemInventoryService(item_repo, room_repo, type_repo, item_inventory_repo, all_inventories_repo)
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWindow(inventory_service)
    myapp.setup_all_inv_tables()
    myapp.setup_items_table()
    myapp.make_inactive_stage()
    myapp.show()
    sys.exit(app.exec_())



