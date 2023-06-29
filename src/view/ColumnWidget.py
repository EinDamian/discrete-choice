from __future__ import annotations
import os

from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5 import uic

from src.controller.functions.DerivativeController import DerivativeController

class ColumnWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/columns.ui', self)

        self.__controller: DerivativeController = DerivativeController()

    def update(self):
        super().update()

    def add(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def remove(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def change(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def export(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def import_(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
