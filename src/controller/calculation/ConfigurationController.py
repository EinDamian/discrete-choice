from __future__ import annotations

from PyQt5.QtWidgets import QTableWidgetItem

from src.controller.AbstractController import AbstractController


class ConfigurationController(AbstractController):
    def select_config(self, index: int):
        self.get_project().select_config(index)

    def update_settings_item(self, item: QTableWidgetItem):
        pp = self.get_project()
        index = pp.get_selected_config_index
        settings = pp.get_config_settings
        # change settings with info from item
        pp.set_config_settings(index, settings)

    def get_config_display_names(self) -> list[str]:
        return self.get_project().get_config_display_names()
