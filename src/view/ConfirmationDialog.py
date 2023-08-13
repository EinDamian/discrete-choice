from PyQt5.QtWidgets import QMessageBox, QWidget


class ConfirmationDialog:
    """Class that offers Confirmation Dialogs"""
    
    def confirm(self, parent: QWidget, msg: str) -> bool:
        """Gets Confirmation of the Message from the User.

        Args:
            parent (QWidget): The Parent Widget of the Dialogwindow.
            msg (str): The Message the User should confirm.

        Returns:
            bool: True if the User gave Confirmation, else False.
        """
        reply = QMessageBox.question(parent, None, msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False