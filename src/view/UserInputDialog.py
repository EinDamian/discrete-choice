from PyQt5.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QLabel, 
    QLineEdit, 
    QPushButton, 
)

class UserInputDialog(QDialog):
    """User Dialog used for the input of information."""
    def __init__(self, input_fields: list[str], button_name: str, window_title: str, parent=None, optional_input_fields: list=[]):
        """Constructor of the user input dialog.

        Args:
            input_fields (list[str]): The labels of the fields that can be input.
            button_name (str): The name shown on the button, that accepts the user input and gets the input.
            window_title (str): The title shown on the dialog.
            parent (_type_, optional): The Widget where it will be displayed. Defaults to None.
            optional_input_fields (list, optional): Fields that are not necessary. Defaults to [].
        """
        super().__init__(parent)
        self.setWindowTitle(f'{window_title}:')

        self.input_fields = input_fields
        self.labels = []
        self.input = []
        self.optional_input_fields = optional_input_fields
        
        for input_field in input_fields:
            self.labels.append(QLabel(f'{input_field}:'))
            self.input.append(QLineEdit())
        
        self.button = QPushButton(button_name)
        self.button.clicked.connect(self.accept_input)

        layout = QVBoxLayout()
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
            if not field_input.text() and field_name not in self.optional_input_fields:
                return False
        self.accept()


    def get_user_input(self) -> list:
        """Retrieves the user input from the dialog.

        Returns:
            list: The input of the user in the same order as the headers.
        """
        return [field_input.text() for field_input in self.input]
