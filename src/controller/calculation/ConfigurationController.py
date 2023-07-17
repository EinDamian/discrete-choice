from __future__ import annotations

from PyQt5.QtWidgets import QTableWidgetItem

from src.controller.AbstractController import AbstractController


class ConfigurationController(AbstractController):
    def select_config(self, index: int):
        try:
            self.get_project().set_selected_config_index(index)
        except IndexError as i_e:
            return i_e

    def update_settings_item(self, variable: str, item: QTableWidgetItem):
        try:
            pp = self.get_project()
            index = pp.get_selected_config_index()
            settings = pp.get_config_settings()
            my_dict = settings[index]
            # TODO: item.text() überprüfen auf Richtigkeit
            my_dict[variable] = item.text()
            pp.set_config_settings(index, my_dict)
        except IndexError as i_e:
            return i_e
        except KeyError as k_e:
            return k_e

    def get_config_display_names(self) -> list[str]:
        return self.get_project().get_config_display_names()
