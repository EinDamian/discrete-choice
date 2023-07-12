from __future__ import annotations

import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QDialog, QVBoxLayout, QSizePolicy, QMainWindow

from src.view import ThresholdField
from src.view.ThresholdField import ThresholdField


class ThresholdWindow(QDialog):
    applyClicked = pyqtSignal(dict)  # this signal is emitted when apply is clicked, it stores the new thresholds

    def __init__(self, thresholds: dict):
        super().__init__()
        self.setWindowTitle("Enter Thresholds")
        self.thresholds = thresholds

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/thresholdwindow.ui', self)  # load ui file created with Qt Creator

        self.scroll_area = self.findChild(QWidget, "scrollArea")  # The scroll area object
        self.container = QWidget()  # This widget is a container for layout
        self.layout = QVBoxLayout()  # With this we can add multiple QLineEdit objects
        self.scroll_area.setWidgetResizable(True)
        self.container.setLayout(self.layout)
        self.scroll_area.setWidget(self.container)

        self.__apply_button = self.findChild(QPushButton, 'apply_button')
        self.__apply_button.clicked.connect(self.apply)
        self.__cancel_button = self.findChild(QPushButton, 'cancel_button')
        self.__cancel_button.clicked.connect(self.close)
        self.__thresholds_control: list[ThresholdField] = self.add_fields(len(self.thresholds))

        # TODO: Complete this class

    def add_fields(self, num: int):
        thresholds_control: list[ThresholdField] = []
        for i in range(num):
            new_field = ThresholdField()
            new_field.set_threshold_value(list(self.thresholds.values())[i])
            new_field.set_label(list(self.thresholds.keys())[i])
            new_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            new_field.setMinimumSize(200, 0)
            self.layout.addWidget(new_field)
            self.layout.addStretch(1)
            thresholds_control.append(new_field)
        return thresholds_control

    def get_user_thresholds(self):
        thresholds_input = {}
        for field in self.__thresholds_control:
            thresholds_input[field.get_label()] = \
                field.get_threshold_input()
        return thresholds_input

    def apply(self):
        self.applyClicked.emit(self.get_user_thresholds())
