from __future__ import annotations
import os

from PyQt5.QtWidgets import QWidget, QLineEdit, QTreeWidget, QTreeWidgetItem
from PyQt5 import uic

from src.controller.calculation.ConfigurationController import ConfigurationController

class ProcessingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/processing_info.ui', self)

        self.__table: QTreeWidget = None
        self.__search_bar: QLineEdit = None
        self.__controller: ConfigurationController = None

    def update(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_selected_config(self, index: int):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_config_settings_item(self, item: QTreeWidgetItem):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
