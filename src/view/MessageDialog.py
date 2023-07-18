from PyQt5.QtWidgets import QMessageBox


class MessageDialog(QMessageBox):
    def __init__(self, title: str, message: str):
        super().__init__()

        self.setWindowTitle(title)
        self.setText(message)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setDefaultButton(QMessageBox.No)
        self.button_clicked = self.exec_()

    def get_decision(self):
        if self.button_clicked == QMessageBox.Yes:
            return True
        return False
