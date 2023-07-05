from __future__ import annotations

from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport
from src.model.processing.Threshold import Threshold

import pandas as pd


class Project:
    @property
    def path(self) -> str:
        raise NotImplementedError

    def undo(self) -> Project:
        raise NotImplementedError

    def redo(self) -> Project:
        raise NotImplementedError

    @property
    def selected_config_index(self) -> int:
        raise NotImplementedError

    @selected_config_index.setter
    def selected_config_index(self, index: int):
        raise NotImplementedError

    @property
    def config_settings(self) -> list[pd.DataFrame]:
        raise NotImplementedError

    def set_config_settings(self, index: int, settings: pd.DataFrame):
        raise NotImplementedError

    @property
    def config_display_names(self) -> list[str]:
        raise NotImplementedError

    def evaluate(self):
        raise NotImplementedError

    @property
    def is_optimizable(self) -> bool:
        raise NotImplementedError

    def optimize_model(self):
        raise NotImplementedError

    def get_raw_data(self, with_derivatives: bool = False) -> pd.DataFrame:
        raise NotImplementedError

    def set_raw_data(self, data: pd.DataFrame):
        raise NotImplementedError

    @property
    def derivatives(self) -> dict[str, FunctionalExpression]:
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

    @property
    def alternatives(self) -> dict[str, FunctionalExpression]:
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

    @property
    def thresholds(self) -> dict[str, Threshold]:
        raise NotImplementedError

    @thresholds.setter
    def thresholds(self, **thresholds: Threshold):
        raise NotImplementedError

    @property
    def evaluation(self) -> pd.DataFrame:
        raise NotImplementedError
