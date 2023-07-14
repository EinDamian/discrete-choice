import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLabel, QDoubleSpinBox

from src.config import ConfigThresholdField as Cfg


class ThresholdField(QWidget):
    """
    This represents the field in the ThresholdWindow, where the user can enter a threshold value for each column
    """
    def __init__(self):
        """
        Initializes a new field
        """
        super().__init__()
        uic.loadUi(f'{os.path.dirname(__file__)}/ui/thresholdfield.ui', self)  # load ui file created with Qt Creator

        self.text_field = self.findChild(QLabel, 'column_name')
        self.value_field = self.findChild(QDoubleSpinBox, 'threshold_value')
        self.value_field.setMaximum(Cfg.MAX_THRESHOLD_VALUE)
        self.value_field.setMinimum(Cfg.MIN_THRESHOLD_VALUE)

    def set_label(self, label):
        """
        sets the name of column (text_field)
        @param label: the column's name
        @type label: str
        """
        self.text_field.setText(label)

    def get_label(self):
        """
        gets the name of the column.
        @return: the column's name (label)
        @rtype: str
        """
        return self.text_field.text()

    def set_threshold_value(self, value):
        """
        sets the threshold in the value_field.
        the value here is the most recent threshold, that the user have entered before
        @param value: the last known threshold
        @type value: float
        """
        self.value_field.setValue(value)

    def get_threshold_input(self):
        """
        gets the value (threshold) from the value_field
        @return: the threshold, which the user wishes to apply currently
        @rtype: float
        """
        return self.value_field.value()
