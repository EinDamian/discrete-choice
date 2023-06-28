from __future__ import annotations

from data.functions.FunctionalExpression import FunctionalExpression
from data.functions.ErrorReport import ErrorReport
from processing.Threshold import Threshold

import pandas as pd

class Project:
    @staticmethod
    def open(path: str) -> Project:
        raise NotImplementedError

    def save(self, path: str = None):
        raise NotImplementedError

    def undo(self) -> Project:
        raise NotImplementedError

    def redo(self) -> Project:
        raise NotImplementedError

    def select_config(self, index: int):
        raise NotImplementedError

    def get_selected_config_index(self) -> int:
        raise NotImplementedError

    def get_config_settings(self) -> list[pd.DataFrame]:
        raise NotImplementedError

    def set_config_settings(self, index: int, settings: pd.DataFrame):
        raise NotImplementedError

    def get_config_display_names(self) -> list[str]:
        raise NotImplementedError

    def evaluate(self) -> bool:
        raise NotImplementedError

    @property
    def is_optimizable(self) -> bool:
        raise NotImplementedError

    def optimize_model(self) -> bool:
        raise NotImplementedError

    @property
    def path(self) -> str:
        raise NotImplementedError

    def get_raw_data(self, with_derivatives: bool = False) -> pd.DataFrame:
        raise NotImplementedError

    def set_raw_data(self, data: pd.DataFrame):
        raise NotImplementedError

    def get_derivatives(self) -> dict[str, FunctionalExpression]:
        raise NotImplementedError

    def set_derivative(self, label: str, function: FunctionalExpression):
        raise NotImplementedError

    def remove_derivative(self, label: str):
        raise NotImplementedError

    def import_derivative(self, path: str):
        raise NotImplementedError

    def export_derivative(self, label: str, path: str):
        raise NotImplementedError

    def get_derivative_error_report(self, label: str) -> ErrorReport:
        raise NotImplementedError

    def get_alternatives(self) -> dict[str, FunctionalExpression]:
        raise NotImplementedError

    def set_alternative(self, label: str, function: FunctionalExpression):
        raise NotImplementedError

    def remove_alternative(self, label: str):
        raise NotImplementedError

    def import_alternative(self, path: str):
        raise NotImplementedError

    def export_alternative(self, label: str, path: str):
        raise NotImplementedError

    def get_alternative_error_report(self, label: str) -> ErrorReport:
        raise NotImplementedError

    def get_thresholds(self) -> dict[str, Threshold]:
        raise NotImplementedError

    def set_thresholds(self, **thresholds: Threshold):
        raise NotImplementedError

    def get_evaluation(self) -> pd.DataFrame:
        raise NotImplementedError
