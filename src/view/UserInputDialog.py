from PyQt5.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QPlainTextEdit
)
from PyQt5.QtGui import QIntValidator
from PyQt5 import QtCore
from src.config import ConfigUserInputWindow

class UserInputDialog(QDialog):
    """User Dialog used for the input of information."""
    def __init__(self, input_fields: list[str], button_name: str, window_title: str, parent=None, 
        optional_input_fields: list = None, numerical_input_fields: list[str] = None):
        """Constructor of the user input dialog.

        Args:
            input_fields (list[str]): The labels of the fields that can be input.
            button_name (str): The name shown on the button, that accepts the user input and gets the input.
            window_title (str): The title shown on the dialog.
            parent (_type_, optional): The Widget where it will be displayed. Defaults to None.
            optional_input_fields (list, optional): Fields that are not necessary. Defaults to [].
        """
        if optional_input_fields is None:
            optional_input_fields = []
        if numerical_input_fields is None:
            numerical_input_fields = []

        super().__init__(parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle(f'{window_title}:')

        self.input_fields = input_fields
        self.labels = []
        self.input = []
        self.optional_input_fields = optional_input_fields
        
        # fist input field is small:
        self.labels.append(QLabel(f'{input_fields[0]}:'))
        self.input.append(QLineEdit())
        
        remaining_input_fields = input_fields[1:]
        
        for input_field in remaining_input_fields:
            self.labels.append(QLabel(f'{input_field}:'))
            text_edit = QPlainTextEdit()
            self.input.append(text_edit)
            
        for input_field in numerical_input_fields:
            self.labels.append(QLabel(f'{input_field}:'))
            int_input = QLineEdit()
            int_input.setValidator(QIntValidator())
            self.input.append(int_input)
        
        self.button = QPushButton(button_name)
        self.button.clicked.connect(self.accept_input)

        layout = QVBoxLayout()
        
        question_mark_label = QLabel("ⓘ")
        question_mark_label.setToolTip(ConfigUserInputWindow.SYNTAX_HELP)
        layout.addWidget(question_mark_label)
        
        for label, input_widget in zip(self.labels, self.input):
            layout.addWidget(label)
            layout.addWidget(input_widget)
            
        layout.addWidget(self.button)
        self.setLayout(layout)

    def accept_input(self) -> bool:
        """Checks if all necessary input field have input.

        Returns:
            bool: False if not all input is there.
        """
        for field_name, field_input in zip(self.input_fields, self.input):
            if field_name not in self.optional_input_fields:
                try:
                    if not field_input.text():
                        return False
                except AttributeError:
                    if len(field_input.toPlainText().replace("\n", "")) == 0:
                        return False
        self.accept()

    def get_user_input(self) -> list:
        """Retrieves the user input from the dialog.

        Returns:
            list: The input of the user in the same order as the headers.
        """
        input = []
        for field_input in self.input:
            try:
                input.append(field_input.text())
            except AttributeError:
                input.append(field_input.toPlainText().replace("\n", ""))
        return input
