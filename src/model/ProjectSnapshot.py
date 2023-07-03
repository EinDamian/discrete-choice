from __future__ import annotations

from src.model.Project import Project
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport
from src.model.data.Model import Model
from src.model.processing.ProcessingConfig import ProcessingConfig
from src.model.processing.Evaluation import Evaluation
from src.model.processing.Threshold import Threshold

import pandas as pd

class ProjectSnapshot(Project):
    def __init__(self):
        self.__previous: ProjectSnapshot | None = None
        self.__next: ProjectSnapshot | None = None
        self.__model: Model = None
        self.__processing_configs: list[ProcessingConfig] = None
        self.__selected_config_index: int = None
        self.__evaluation: Evaluation | None = None
        self.__thresholds: dict[str, Threshold] = None

        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def __copy__(self):
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
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

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
