from __future__ import annotations

from PySide6.QtWidgets import QWidget, QLineEdit, QTreeWidget, QTreeWidgetItem

from ..controller.calculation.ConfigurationController import ConfigurationController

class ProcessingWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.__table: QTreeWidget = None
        self.__search_bar: QLineEdit = None
        self.__controller: ConfigurationController = None

    def update(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_selected_config(self, index: int):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_config_settings_item(self, item: QTreeWidgetItem):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
