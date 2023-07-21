from __future__ import annotations

from src.config import ConfigProcessingWidget
from src.controller.AbstractController import AbstractController
from src.model.data.functions.ErrorReport import ErrorReport
from src.model.data.functions.FunctionalExpression import FunctionalExpression


class ConfigurationController(AbstractController):
    """Controller used to control all changes regarding the configurations."""
    def select_config(self, index: int):
        """
        sets the chosen config index
        :param index: index of the chosen config
        :raises IndexError
        """
        try:
            self.get_project().set_selected_config_index(index)
        except IndexError as i_e:
            raise i_e

    def update_settings_item(self, name: str, value: str):
        """
        updates the config settings and also the choice variable, if it is updated
        :param name: the variables name
        :param value: the variables expression
        :raises: IndexError
        :raises: KeyError
        """
        try:
            project = self.get_project()
            index = project.get_selected_config_index()
            settings = project.get_config_settings()
            my_dict = settings[index]
            expression = FunctionalExpression(value)
            if name == ConfigProcessingWidget.CHOICE:
                self.get_project().set_choice(expression)
            else:
                my_dict[name] = expression
                project.set_config_settings(index, my_dict)
            self.save()
        except IndexError as i_e:
            raise i_e
        except KeyError as k_e:
            raise k_e

    def get_error_report(self, label: str) -> ErrorReport:
        """
        gets the error report for the given label
        :param label:
        :return:
        """
        raise NotImplementedError  # TODO: ?

    def get_config_display_names(self) -> list[str]:
        """
        accessing method for all the config display names
        :return: list of the names as strings
        """
        return self.get_project().get_config_display_names()
