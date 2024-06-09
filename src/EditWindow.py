from PySide6.QtWidgets import (
    QVBoxLayout,
    QDialog, 
    QLineEdit, 
    QFormLayout, 
    QDialogButtonBox,
    QComboBox
)

import ETools

class EditDialog(QDialog):
    def __init__(self, name, location, type_, url, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Entry")
        self.resize(400, 200)

        self.name_input = QLineEdit(name)
        self.location_input = QLineEdit(location)
        self.type_input = QComboBox()
        self.type_input.addItems(ETools.SupportedTypes)
        self.type_input.setCurrentText(type_)
        self.url_input = QLineEdit(url)

        form_layout = QFormLayout()
        form_layout.addRow(ETools.Key_Column1, self.name_input)
        form_layout.addRow(ETools.Key_Column2, self.location_input)
        form_layout.addRow(ETools.Key_Column3, self.type_input)
        form_layout.addRow(ETools.Key_Column4, self.url_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_data(self):
        return self.name_input.text(), self.location_input.text(), self.type_input.currentText(), self.url_input.text()