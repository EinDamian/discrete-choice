from __future__ import annotations

from src.controller.AbstractController import AbstractController
from src.model.data.functions.ErrorReport import ErrorReport
from src.model.data.functions.FunctionalExpression import FunctionalExpression


class ConfigurationController(AbstractController):
    def select_config(self, index: int):
        try:
            self.get_project().set_selected_config_index(index)
        except IndexError as i_e:
            return i_e

    def update_settings_item(self, variable: str, value: str):
        try:
            pp = self.get_project()
            index = pp.get_selected_config_index()
            settings = pp.get_config_settings()
            my_dict = settings[index]
            expression = FunctionalExpression(value)
            if variable == "$CHOICE":
                self.get_project().set_choice(expression)
            else:
                my_dict[variable] = expression
                pp.set_config_settings(index, my_dict)
            self.save()
        except IndexError as i_e:
            return i_e
        except KeyError as k_e:
            return k_e

    def get_error_report(self, label: str) -> ErrorReport:
        raise NotImplementedError  # TODO: ?

    def get_config_display_names(self) -> list[str]:
        return self.get_project().get_config_display_names()
