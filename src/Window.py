import sys
import subprocess
from PySide6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QPushButton, 
    QTableWidget, 
    QTableWidgetItem, 
    QCheckBox, 
    QHeaderView, 
    QAbstractItemView, 
    QDialog,
    QSpacerItem,
    QSizePolicy,
    QTextEdit
)
from PySide6.QtCore import Qt
from EditWindow import EditDialog
import ETools

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("External Assets")
        self.resize(600, 400)

        main_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["", ETools.Key_Column1, ETools.Key_Column2, ETools.Key_Column3, ETools.Key_Column4])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        db_data = ETools.ETools.load_json()
        if db_data is not None:
            for array_item in db_data:
                name        = array_item[ETools.Key_Column1]
                location    = array_item[ETools.Key_Column2]
                type_       = array_item[ETools.Key_Column3]
                url         = array_item[ETools.Key_Column4]

                self.add_table_item(False, name, location, type_, url)


        self.table.cellDoubleClicked.connect(self.open_edit_dialog)

        main_layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        
        select_all_button = QPushButton("Select All")
        none_button = QPushButton("None")
        delete_button = QPushButton("Delete")
        add_button = QPushButton("Add")
        run_button = QPushButton("Run")

        add_button.clicked.connect(self.add_new_row)
        delete_button.clicked.connect(self.delete_selected_row)
        select_all_button.clicked.connect(self.select_all)
        none_button.clicked.connect(self.deselect_all)
        run_button.clicked.connect(self.run_processes)
        
        button_layout.addWidget(select_all_button)
        button_layout.addWidget(none_button)
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(delete_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(run_button)

        main_layout.addLayout(button_layout)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        main_layout.addWidget(self.console)
        
        self.setLayout(main_layout)
    
    @staticmethod
    def show_window():
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

    def add_table_item(self, status, name, location, type_, url):
        checkbox = QCheckBox()
        checkbox.checkState = status
        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_widget)
        checkbox_layout.addWidget(checkbox)
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setCellWidget(row, 0, checkbox_widget)
        self.table.setItem(row, 1, QTableWidgetItem(name))
        self.table.setItem(row, 2, QTableWidgetItem(location))
        self.table.setItem(row, 3, QTableWidgetItem(type_))
        self.table.setItem(row, 4, QTableWidgetItem(url))
    
    def open_edit_dialog(self, row, column):
        name        = self.table.item(row, 1).text()
        location    = self.table.item(row, 2).text()
        type_       = self.table.item(row, 3).text()
        url         = self.table.item(row, 4).text()

        dialog = EditDialog(name, location, type_, url, self)
        if dialog.exec() == QDialog.Accepted:
            name, location, type_, url = dialog.get_data()

            self.table.item(row, 1).setText(name)
            self.table.item(row, 2).setText(location)
            self.table.item(row, 3).setText(type_)
            self.table.item(row, 4).setText(url)
            
            self.save_data()
    
    def add_new_row(self):
        self.add_table_item(False, "", "", "", "")

    def delete_selected_row(self):
        current_row = self.table.currentRow()
        if current_row != -1:
            self.table.removeRow(current_row)
            self.save_data()
    
    def select_all(self):
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0).layout().itemAt(0).widget()
            checkbox.setChecked(True)
    
    def deselect_all(self):
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0).layout().itemAt(0).widget()
            checkbox.setChecked(False)
    
    def save_data(self):
        data = []
        for row in range(self.table.rowCount()):
            item_data = {
                ETools.Key_Column1: self.table.item(row, 1).text(),
                ETools.Key_Column2: self.table.item(row, 2).text(),
                ETools.Key_Column3: self.table.item(row, 3).text(),
                ETools.Key_Column4: self.table.item(row, 4).text()
            }
            data.append(item_data)
        
        ETools.ETools.save_json(data)
    
    def run_processes(self):
        db_data = ETools.ETools.load_json()

        for item_data in db_data:
            file_url = item_data[ETools.Key_Column4]
            command = ["C:/Users/admin/Documents/GitHub/ExternalsTool/Tools/megatools/megatools.exe", "dl", "--path", ETools.ETools.ConfigFolder, file_url]

            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            for line in process.stdout:
                self.console.append(line.strip())
                QApplication.processEvents()

            process.wait()