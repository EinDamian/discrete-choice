from __future__ import annotations

from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport
from src.model.processing.Threshold import Threshold

import pandas as pd


class Project:
    """
    This interface represents an abstract Project with its operations.
    """

    @property
    def path(self) -> str:
        """
        :return: Path of the project. On this path the project will be saved on default.
        :rtype: str
        """
        raise NotImplementedError

    def undo(self) -> Project:
        """
        Reverts the last done change in the project.
        :return: Project interface before last change.
        :rtype: Project
        """
        raise NotImplementedError

    def redo(self) -> Project:
        """
        Reverts the last undo operation in the project.
        :return: Project interface before the last undo operation.
        :rtype: Project
        """
        raise NotImplementedError

    def get_selected_config_index(self) -> int:
        """
        :return: Index of current selected process configuration.
        :rtype: int
        """
        raise NotImplementedError

    def set_selected_config_index(self, index: int):
        """
        Updates the selected process configuration.
        :param index: New index of process configuration, which should be selected.
        :type index: int
        """
        raise NotImplementedError

    def get_config_settings(self) -> list[pd.DataFrame]:
        """
        :return: List of the settings of all process configurations.
        :rtype: list[pd.DataFrame]
        """
        raise NotImplementedError

    def set_config_settings(self, index: int, settings: pd.DataFrame):
        """
        Updates the settings of a single process configuration.
        :param index: Index of the process configuration in the project, which should be updated.
        :type index: int
        :param settings: New settings, which should be set.
        :type settings: pd.DataFrame
        """
        raise NotImplementedError

    def get_config_display_names(self) -> list[str]:
        """
        :return: List of the display names of all process configurations in the project.
        :rtype: list[str]
        """
        raise NotImplementedError

    def evaluate(self):
        """
        Starts evaluating the model based on the selected processing configuration.
        """
        raise NotImplementedError

    def is_optimizable(self) -> bool:
        """
        :return: Truth value, whether an evaluation exists, which is able to optimize the model.
        :rtype: bool
        """
        raise NotImplementedError

    def optimize_model(self):
        """
        Starts optimizing the model based on a before calculated evaluation.
        """
        raise NotImplementedError

    def get_raw_data(self, with_derivatives: bool = False) -> pd.DataFrame:
        """
        Returns the data which is stored in the model.
        :param with_derivatives: Determines, whether all derivatives should be added to raw data.
        :type with_derivatives: bool
        :return: Table with all raw data and (if selected) all calculated derivatives.
        :rtype: pd.DataFrame
        """
        raise NotImplementedError

    def set_raw_data(self, data: pd.DataFrame):
        """
        Updates the raw data stored in the model.
        :param data: New raw data, which should be set.
        :type data: pd.DataFrame
        """
        raise NotImplementedError

    def get_derivatives(self) -> dict[str, FunctionalExpression]:
        """
        :return: Dictionary of all derivatives stored in the model with label and expression.
        :rtype: dict[str, FunctionalExpression]
        """
        raise NotImplementedError

    def set_derivative(self, label: str, function: FunctionalExpression):
        """
        Sets a derivative in the model.
        :param label: Label of derivative, which should be set.
        :type label: str
        :param function: Expression of derivative.
        :type function: FunctionalExpression
        """
        raise NotImplementedError

    def remove_derivative(self, label: str):
        """
        Removes a derivative from the model.
        :param label: Label of derivative, which should be removed.
        :type label: str
        """
        raise NotImplementedError

    def get_derivative_error_report(self, label: str) -> ErrorReport:
        """
        Returns error report of a derivative stored in the model.
        :param label: Label of derivative.
        :type label: str
        :return: Error report of the requested derivative.
        :rtype: ErrorReport
        """
        raise NotImplementedError

    def get_alternatives(self) -> dict[str, FunctionalExpression]:
        """
        :return: Dictionary of all alternatives stored in the model with label and expression.
        :rtype: dict[str, FunctionalExpression]
        """
        raise NotImplementedError

    def set_alternative(self, label: str, function: FunctionalExpression):
        """
        Sets an alternative in the model.
        :param label: Label of alternative, which should be set.
        :type label: str
        :param function: Expression of alternative.
        :type function: FunctionalExpression
        """
        raise NotImplementedError

    def remove_alternative(self, label: str):
        """
        Removes an alternative from the model.
        :param label: Label of alternative, which should be removed.
        :type label: str
        """
        raise NotImplementedError

    def get_alternative_error_report(self, label: str) -> ErrorReport:
        """
        Returns error report of an alternative stored in the model.
        :param label: Label of alternative.
        :type label: str
        :return: Error report of the requested alternative.
        :rtype: ErrorReport
        """
        raise NotImplementedError

    def get_thresholds(self) -> dict[str, Threshold]:
        """
        :return: Dictionary of all visualization thresholds with label and threshold.
        :rtype: dict[str, Threshold]
        """
        raise NotImplementedError

    def set_thresholds(self, **thresholds: Threshold):
        """
        Replaces all thresholds.
        :param thresholds: Dictionary of new thresholds with label and threshold
        :type: dict[str, Threshold]
        """
        raise NotImplementedError

    def get_evaluation(self) -> pd.DataFrame:
        """
        :return: Evaluation stored in the project.
        :rtype: Evaluation
        """
        raise NotImplementedError
