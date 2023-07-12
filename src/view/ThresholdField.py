import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QDoubleSpinBox


class ThresholdField(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{os.path.dirname(__file__)}/ui/thresholdfield.ui', self)  # load ui file created with Qt Creator

        self.text_field = self.findChild(QLabel, 'column_name')
        self.threshold_input = self.findChild(QDoubleSpinBox, 'threshold_value')

    def set_label(self, label):
        self.text_field.setText(label)

    def get_label(self):
        return self.text_field.text()

    def set_threshold_value(self, value):
        self.threshold_input.setValue(value)

    def get_threshold_input(self):
        return self.threshold_input.value()
