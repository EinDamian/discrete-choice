from __future__ import annotations

from Project import Project
from ProjectSnapshot import ProjectSnapshot
from data.functions.FunctionalExpression import FunctionalExpression
from data.functions.ErrorReport import ErrorReport
from processing.Threshold import Threshold

import pandas as pd

class ProxyProject(Project):
    def __init__(self):
        self.__current_project: ProjectSnapshot = None
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def save(self, path: str = None):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def undo(self) -> Project:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def redo(self) -> Project:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def select_config(self, index: int):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_selected_config_index(self) -> int:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_config_settings(self) -> list[pd.DataFrame]:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_config_settings(self, index: int, settings: pd.DataFrame):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_config_display_names(self) -> list[str]:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def evaluate(self) -> bool:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    @property
    def is_optimizable(self) -> bool:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def optimize_model(self) -> bool:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    @property
    def path(self) -> str:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_raw_data(self, with_derivatives: bool = False) -> pd.DataFrame:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_raw_data(self, data: pd.DataFrame):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_derivatives(self) -> dict[str, FunctionalExpression]:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_derivative(self, label: str, function: FunctionalExpression):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def remove_derivative(self, label: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def import_derivative(self, path: str):
        raise NotImplementedError

    def export_derivative(self, label: str, path: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_derivative_error_report(self, label: str) -> ErrorReport:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_alternatives(self) -> dict[str, FunctionalExpression]:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_alternative(self, label: str, function: FunctionalExpression):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def remove_alternative(self, label: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def import_alternative(self, path: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def export_alternative(self, label: str, path: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_alternative_error_report(self, label: str) -> ErrorReport:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_thresholds(self) -> dict[str, Threshold]:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_thresholds(self, **thresholds: Threshold):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_evaluation(self) -> pd.DataFrame:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
