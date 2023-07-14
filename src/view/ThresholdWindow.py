from __future__ import annotations

import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QDialog, QVBoxLayout, QSizePolicy

from src.view import ThresholdField
from src.view.ThresholdField import ThresholdField


class ThresholdWindow(QDialog):
    """
    This class represents the threshold window, where
    the user can enter new thresholds and apply them.
    """

    '''
    this following signal is emitted when apply is clicked, it stores the new thresholds as adict
    '''
    applyClicked = pyqtSignal(dict)

    def __init__(self, thresholds: dict):
        """
        Initializes a new threshold Window
        @param thresholds: the thresholds, which the user have entered before
        @type thresholds: dictionary, with column's names as keys and the actual thresholds as values
        """
        super().__init__()
        self.thresholds = thresholds

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/thresholdwindow.ui', self)  # load ui file created with Qt Creator

        self.scroll_area = self.findChild(QWidget, "scrollArea")  # The scroll area object
        self.container = QWidget()  # This widget is a container for layout
        self.layout = QVBoxLayout()  # With this we can add multiple ThresholdsField objects
        self.scroll_area.setWidgetResizable(True)
        self.container.setLayout(self.layout)
        self.scroll_area.setWidget(self.container)

        self.__apply_button = self.findChild(QPushButton, 'apply_button')
        self.__apply_button.clicked.connect(self.apply)
        self.__cancel_button = self.findChild(QPushButton, 'cancel_button')
        self.__cancel_button.clicked.connect(self.close)
        self.__thresholds_control: list[ThresholdField] = self.add_fields(len(self.thresholds))

    def add_fields(self, num: int):
        """
        This functions adds as many threshold-fields as the number of columns in the data
        to the layout in the ThresholdWindow (GUI)
        @param num: number of columns
        @type num: int
        @return: the list, which contains all the threshold-fields in
                the same order as the columns are given
        @rtype: list
        """
        thresholds_control: list[ThresholdField] = []
        for i in range(num):
            new_field = ThresholdField()

            new_field.set_label(list(self.thresholds.keys())[i])
            new_field.set_threshold_value(list(self.thresholds.values())[i])

            new_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            new_field.setMinimumSize(200, 0)
            self.layout.addWidget(new_field)
            self.layout.addStretch(1)

            thresholds_control.append(new_field)
        return thresholds_control

    def get_user_thresholds(self):
        """
        gets the thresholds from the fields
        @return: dictionary, which contains the column's names as
        keys and the actual thresholds as values
        @rtype: dict
        """
        thresholds_input = {}
        for field in self.__thresholds_control:
            thresholds_input[field.get_label()] = \
                field.get_threshold_input()
        return thresholds_input

    def apply(self):
        """
        requests the thresholds, which the user has entered, signals the creator class (EvaluationWidget)
        about the user's wish to apply the thresholds and passes their values to the class.
        """
        self.applyClicked.emit(self.get_user_thresholds())
        self.close()
