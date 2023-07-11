from __future__ import annotations
import os

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QComboBox
from PyQt5 import uic

from src.controller.calculation.ConfigurationController import ConfigurationController


class ProcessingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/processing_info.ui', self)  # load ui file created with Qt Creator

        self.__controller: ConfigurationController = ConfigurationController()
        combo_box = self.findChild(QComboBox, "combo_process_type")
        #config_names = self.__controller.get_project().get_config_display_names()
        #for name in config_names:
        #    combo_box.addItem(name)

    def update(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_selected_config(self, index: int):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_config_settings_item(self, item: QTreeWidgetItem):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
