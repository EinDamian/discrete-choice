from __future__ import annotations

from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit

class ThresholdWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.__apply_button: QPushButton = None
        self.__cancel_button: QPushButton = None
        self.__thresholds_control: list[QLineEdit] = None

        raise NotImplementedError  # TODO: IMPLEMENTIEREN
