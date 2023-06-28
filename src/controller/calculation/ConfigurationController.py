from __future__ import annotations

from ..AbstractController import AbstractController
from PySide6.QtWidgets import QTableWidgetItem

class ConfigurationController(AbstractController):
    def select_config(self, index: int):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def update_settings_item(self, item: QTableWidgetItem):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
