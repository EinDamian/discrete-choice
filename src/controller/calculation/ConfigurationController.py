from __future__ import annotations

from PyQt5.QtWidgets import QTableWidgetItem

from src.controller.AbstractController import AbstractController

class ConfigurationController(AbstractController):
    def select_config(self, index: int):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def update_settings_item(self, item: QTableWidgetItem):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
