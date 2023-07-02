from __future__ import annotations
import os

from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

from src.controller.functions.AlternativeController import AlternativeController

class ModelWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/model.ui', self)  # load ui file created with Qt Creator

        self.__controller: AlternativeController = AlternativeController()

        addButton = self.findChild(QToolButton, "add_button")
        addButton.clicked.connect(self.add)
        exportButton = self.findChild(QToolButton, "export_button")
        exportButton.clicked.connect(self.export)
        importButton = self.findChild(QToolButton, "import_button")
        importButton.clicked.connect(self.import_)
        removeButton = self.findChild(QToolButton, "remove_button")
        removeButton.clicked.connect(self.remove)

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
