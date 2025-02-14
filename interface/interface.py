from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem

from services.exceptions import IncorrectItemError, EmptyFieldError
from services.inventory_service import ItemInventoryService
from gui import *
import sys

from services.exceptions import IdAlreadyInventoriedException, EntityCodeIsUsedException


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, inventory_service, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.inventory_service = inventory_service
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.lineEdit.setValidator(QIntValidator(0, 9999999))
        self.ui.typecodeLine.setValidator(QIntValidator(0, 9999999))
        self.ui.roomcodeLine.setValidator(QIntValidator(0, 9999999))
        self.ui.currentInvTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ui.progressBar.setValue(0)
        self.item_inventoried_tuple = ()

        self.ui.startButton.clicked.connect(self.start_inventory)
        self.ui.inventoryIdButton.clicked.connect(self.inventory_item)
        self.ui.finishInvButton.clicked.connect(self.finish_inv)
        self.ui.cancelInvButton.clicked.connect(self.show_confirmation)
        self.ui.additemButton.clicked.connect(self.create_item)
        self.ui.addtypeButton.clicked.connect(self.create_type)
        self.ui.addroomButton.clicked.connect(self.create_room)

    def make_inactive_stage(self):
        self.ui.inventoryIdButton.setEnabled(False)
        self.ui.inventoryIdButton.setStyleSheet("opacity: 0.5;")
        self.ui.finishInvButton.setEnabled(False)
        self.ui.finishInvButton.setStyleSheet("opacity: 0.5;")
        self.ui.cancelInvButton.setEnabled(False)
        self.ui.cancelInvButton.setStyleSheet("opacity: 0.5;")
        self.ui.lineEdit.setEnabled(False)
        self.ui.lineEdit.setStyleSheet("opacity: 0.5;")
        self.ui.startButton.setEnabled(True)
        self.ui.startButton.setStyleSheet("opacity: 1;")

    def make_active_stage(self):
        self.ui.inventoryIdButton.setEnabled(True)
        self.ui.inventoryIdButton.setStyleSheet("opacity: 1;")
        self.ui.finishInvButton.setEnabled(True)
        self.ui.finishInvButton.setStyleSheet("opacity: 1;")
        self.ui.cancelInvButton.setEnabled(True)
        self.ui.cancelInvButton.setStyleSheet("opacity: 1;")
        self.ui.lineEdit.setEnabled(True)
        self.ui.lineEdit.setStyleSheet("opacity: 1;")
        self.ui.startButton.setEnabled(False)
        self.ui.startButton.setStyleSheet("opacity: 0.5;")

    def setup_all_inv_tables(self):
        try:
            data = self.inventory_service.get_all_inv_info()
            rows = data[0]
            info = data[1]

            self.ui.inventoriesTable.setRowCount(0)
            self.ui.inventoriesTable.verticalHeader().setVisible(False)

            for i in range(rows):
                self.ui.inventoriesTable.insertRow(i)

                self.ui.inventoriesTable.setItem(i, 0, QTableWidgetItem(str(info[i].id)))
                self.ui.inventoriesTable.setItem(i, 1, QTableWidgetItem(str(info[i].status)))
                self.ui.inventoriesTable.setItem(i, 2, QTableWidgetItem(str(info[i].created_at)))
                self.ui.inventoriesTable.setItem(i, 3, QTableWidgetItem(str(info[i].updated_at)))

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()

    def setup_items_table(self):
        try:
            data = self.inventory_service.get_entities_info("item")
            rows = data[0]
            info = data[1]

            self.ui.itemsTable.setRowCount(0)

            for i in range(rows):
                self.ui.itemsTable.insertRow(i)

                self.ui.itemsTable.setItem(i, 0, QTableWidgetItem(str(info[i].id)))
                self.ui.itemsTable.setItem(i, 1, QTableWidgetItem(str(info[i].name)))
                self.ui.itemsTable.setItem(i, 2, QTableWidgetItem(str(info[i].type)))
                self.ui.itemsTable.setItem(i, 3, QTableWidgetItem(str(info[i].room)))
            self.ui.itemsTable.resizeRowsToContents()

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()

    def setup_types_table(self):
        try:
            data = self.inventory_service.get_entities_info("type")
            rows = data[0]
            info = data[1]

            self.ui.typeTable.setRowCount(0)

            for i in range(rows):
                self.ui.typeTable.insertRow(i)

                self.ui.typeTable.setItem(i, 0, QTableWidgetItem(str(info[i].item_type)))
                self.ui.typeTable.setItem(i, 1, QTableWidgetItem(str(info[i].type_name)))
                self.ui.typeTable.setItem(i, 2, QTableWidgetItem(str(info[i].description)))
            self.ui.typeTable.resizeRowsToContents()

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()



    def setup_rooms_table(self):
        try:
            data = self.inventory_service.get_entities_info("room")
            rows = data[0]
            info = data[1]

            self.ui.roomTable.setRowCount(0)

            for i in range(rows):
                self.ui.roomTable.insertRow(i)

                self.ui.roomTable.setItem(i, 0, QTableWidgetItem(str(info[i].item_room)))
                self.ui.roomTable.setItem(i, 1, QTableWidgetItem(str(info[i].room_name)))
                self.ui.roomTable.setItem(i, 2, QTableWidgetItem(str(info[i].description)))
            self.ui.roomTable.resizeRowsToContents()

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()


    def start_inventory(self):
        try:
            self.item_inventoried_tuple = ()
            current_inv = self.inventory_service.start_inventory()
            current_row = self.ui.inventoriesTable.rowCount()
            self.ui.inventoriesTable.insertRow(current_row)
            self.ui.inventoriesTable.setItem(current_row, 0, QTableWidgetItem(str(current_inv.id)))
            self.ui.inventoriesTable.setItem(current_row, 1, QTableWidgetItem(current_inv.status))
            self.ui.inventoriesTable.setItem(current_row, 2, QTableWidgetItem(current_inv.created_at))
            self.ui.inventoriesTable.setItem(current_row, 3, QTableWidgetItem(current_inv.updated_at))

            self.ui.statusbar.showMessage(f'inventory {self.inventory_service.inventory_id} started')
            self.ui.progressBar.setValue(0)
            self.ui.currentInvTable.setRowCount(0)

            self.make_active_stage()

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()


    def update_progressbar(self):
        total_items = self.inventory_service.total_items
        current_count = self.ui.currentInvTable.rowCount()

        if total_items > 0:
            progress_value = int((current_count / total_items) * 100)
            self.ui.progressBar.setValue(progress_value)



    def inventory_item(self, row_position=None):
        try:
            item_id = self.ui.lineEdit.text()

            result = self.inventory_service.inventory_item(item_id)

            item = []

            item_name = result[0].name
            item_type_name = result[1].type_name
            item_room_name = result[2].room_name

            item.append(item_id)
            item.append(item_name)
            item.append(item_type_name)
            item.append(item_room_name)

            row_position = self.ui.currentInvTable.rowCount()
            self.ui.currentInvTable.insertRow(row_position)

            self.ui.currentInvTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(item_id))
            self.ui.currentInvTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(item_name))
            self.ui.currentInvTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(item_type_name))
            self.ui.currentInvTable.setItem(row_position, 3, QtWidgets.QTableWidgetItem(item_room_name))

            self.item_inventoried_tuple += (item,)

            self.ui.lineEdit.clear()

            self.update_progressbar()

        except IncorrectItemError as e:
            self.ui.statusbar.showMessage(f"Предмет с id {item_id} не найден")
            return
        except IdAlreadyInventoriedException as e:
            self.ui.statusbar.showMessage(f"Предмет с id {item_id} уже был добавлен")
            return

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()


    def finish_inv(self):
        try:
            result = self.inventory_service.finish_inventory()
            found_items = result[0]
            unfound_items = result[1]
            finished_inv = result[2]
            current_row = self.ui.inventoriesTable.rowCount() - 1
            self.ui.inventoriesTable.setItem(current_row, 0, QTableWidgetItem(str(finished_inv.id)))
            self.ui.inventoriesTable.setItem(current_row, 1, QTableWidgetItem(finished_inv.status))
            self.ui.inventoriesTable.setItem(current_row, 2, QTableWidgetItem(finished_inv.created_at))
            self.ui.inventoriesTable.setItem(current_row, 3, QTableWidgetItem(finished_inv.updated_at))

            result_widget = QtWidgets.QMessageBox()
            result_widget.setIcon(QtWidgets.QMessageBox.Information)
            result_widget.setWindowTitle('Inventory results')
            result_widget.setStandardButtons(QtWidgets.QMessageBox.Ok)

            result_text = (
                    "Найденные предметы:\n" +
                    "\n".join([
                        f"ID {item['id']}: {item['name']} (Тип: {item['type']}, Комната: {item['room']})"
                        for item in found_items
                    ]) +
                    "\n\nНе найденные предметы: \n" +
                    "\n".join([
                        f"ID {item['id']}: {item['name']} (Тип: {item['type']}, Комната: {item['room']})"
                        for item in unfound_items
                    ])
            )

            self.add_inv_results_to_table()

            self.make_inactive_stage()

            result_widget.setText(result_text)
            result_widget.exec()
            self.ui.statusbar.showMessage(f'inventory {self.inventory_service.inventory_id} finished')

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()


    def show_confirmation(self):
        cancel_widget = QtWidgets.QMessageBox()
        cancel_widget.setIcon(QtWidgets.QMessageBox.Information)
        cancel_widget.setWindowTitle('Отменить инвентаризацию?')
        cancel_widget.setText("Вы уверены, что хотите отменить?")
        yes_button = cancel_widget.addButton("Да", QtWidgets.QMessageBox.YesRole)
        no_buttion = cancel_widget.addButton("Нет", QtWidgets.QMessageBox.NoRole)

        cancel_widget.exec()

        if cancel_widget.clickedButton() == yes_button:
            self.cancel_process()



    def add_inv_results_to_table(self):
        self.ui.lastInvTable.setRowCount(0)
        for row_position, item in enumerate(self.item_inventoried_tuple):
            self.ui.lastInvTable.insertRow(row_position)
            for col, value in enumerate(item):
                self.ui.lastInvTable.setItem(row_position, col, QtWidgets.QTableWidgetItem(value))



    def cancel_process(self):
        self.ui.currentInvTable.setRowCount(0)
        inv = self.inventory_service.cancel_ongoing_inv()
        row = self.ui.inventoriesTable.rowCount() - 1
        self.ui.inventoriesTable.setItem(row, 1, QTableWidgetItem(inv.status))
        self.make_inactive_stage()
        self.ui.statusbar.showMessage(f'inventory {self.inventory_service.inventory_id} canceled')

    def fill_typebox(self):
        self.ui.itemtypesBox.clear()

        row_count = self.ui.typeTable.rowCount()
        for row in range(row_count):
            item_name = self.ui.typeTable.item(row, 1).text()
            item_id = int(self.ui.typeTable.item(row, 0).text())

            self.ui.itemtypesBox.addItem(item_name, item_id)

    def fill_roombox(self):
        self.ui.itemroomBox.clear()

        row_count = self.ui.roomTable.rowCount()
        for row in range(row_count):
            item_name = self.ui.roomTable.item(row, 1).text()
            item_id = int(self.ui.roomTable.item(row, 0).text())

            self.ui.itemroomBox.addItem(item_name, item_id)

    def create_item(self):
        try:
            name = self.ui.nameLine.text()
            type = self.ui.itemtypesBox.currentData()
            room = self.ui.itemroomBox.currentData()

            if name is None or name.strip() == "":
                self.ui.statusbar.showMessage("Ошибка: поле 'Название' не заполнено")
                return

            item = self.inventory_service.add_entity("item", name, type, room)

            if item is None:
                self.ui.statusbar.showMessage("Ошибка, предмет не был создан")
                return

            row_position = self.ui.itemsTable.rowCount()
            self.ui.itemsTable.insertRow(row_position)

            self.ui.itemsTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(item.id)))
            self.ui.itemsTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(item.name))
            self.ui.itemsTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(item.type)))
            self.ui.itemsTable.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(item.room)))

            self.ui.nameLine.clear()

            self.ui.itemsTable.resizeRowsToContents()

        except EmptyFieldError as e:
            self.ui.statusbar.showMessage(f"Поля ввода для добавления не были заполнены")
            return

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()

    def create_type(self):
        try:
            name = self.ui.typenameLine.text()
            type_id = self.ui.typecodeLine.text()
            desc = self.ui.typedescLine.text()

            if name is None or name.strip() == "":
                self.ui.statusbar.showMessage("Ошибка: поле 'Название' не заполнено")
                return
            if type_id is None or type_id.strip() == "":
                self.ui.statusbar.showMessage("Ошибка: поле 'Тип' не заполнено")
                return
            if desc is None or desc.strip() == "":
                self.ui.statusbar.showMessage("Ошибка: поле 'Описание' не заполнено")
                return

            entity = self.inventory_service.add_entity("type", type_id, name, desc)

            if entity is None:
                self.ui.statusbar.showMessage(f"Id уже занят")
                return

            row_position = self.ui.typeTable.rowCount()
            self.ui.typeTable.insertRow(row_position)

            self.ui.typeTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(entity.item_type)))
            self.ui.typeTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(entity.type_name))
            self.ui.typeTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(entity.description))

            self.ui.typenameLine.clear()
            self.ui.typecodeLine.clear()
            self.ui.typedescLine.clear()

            self.ui.typeTable.resizeRowsToContents()

            self.fill_typebox()

        except EntityCodeIsUsedException as e:
            self.ui.statusbar.showMessage(f"Id уже занят")

        except EmptyFieldError as e:
            self.ui.statusbar.showMessage(f"Поля ввода для добавления не были заполнены")
            return

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()

    def create_room(self):
        try:
            name = self.ui.roomnameLine.text()
            code = self.ui.roomcodeLine.text()
            desc = self.ui.roomdescLine.text()

            if name is None or name.strip() == "":
                self.ui.statusbar.showMessage("Ошибка: поле 'Название' не заполнено")
                return
            if code is None or code.strip() == "":
                self.ui.statusbar.showMessage("Ошибка: поле 'Код' не заполнено")
                return
            if desc is None or desc.strip() == "":
                self.ui.statusbar.showMessage("Ошибка: поле 'Описание' не заполнено")
                return

            entity = self.inventory_service.add_entity("room", code, name, desc)

            row_position = self.ui.roomTable.rowCount()
            self.ui.roomTable.insertRow(row_position)

            self.ui.roomTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(entity.item_room)))
            self.ui.roomTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(entity.room_name))
            self.ui.roomTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(entity.description))

            self.ui.roomnameLine.clear()
            self.ui.roomcodeLine.clear()
            self.ui.roomdescLine.clear()

            self.ui.roomTable.resizeRowsToContents()

            self.fill_roombox()

        except EntityCodeIsUsedException as e:
            self.ui.statusbar.showMessage(f"Код уже занят")

        except EmptyFieldError as e:
            self.ui.statusbar.showMessage(f"Поля ввода для добавления не были заполнены")
            return

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()




















