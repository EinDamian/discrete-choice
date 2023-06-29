from __future__ import annotations

from PyQt5.QtWidgets import QWidget, QToolButton

from src.controller.functions.AlternativeController import AlternativeController

class ModelWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.__add_button: QToolButton = None
        self.__remove_button: QToolButton = None
        self.__import_button: QToolButton = None
        self.__export_button: QToolButton = None
        self.__controller: AlternativeController = None

        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def update(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

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
