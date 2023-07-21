from PyQt5.QtWidgets import QMessageBox


class EvalMessageDialog(QMessageBox):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Evaluation at work...")
        self.setText("The evaluation is currently being calculated."
                     "This Process may take few minutes...")
        self.setStandardButtons(QMessageBox.Abort)
        self.button_clicked = self.exec_()

    def get_abort(self):
        if self.button_clicked == QMessageBox.Abort:
            return True
        return False
