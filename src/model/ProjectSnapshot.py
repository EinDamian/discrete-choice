"""This module contains only one class with the same name."""

from __future__ import annotations

from src.model.Project import Project
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport
from src.model.data.Model import Model
from src.model.processing.ProcessingConfig import ProcessingConfig
from src.model.processing.SimpleProcessingConfig import SimpleProcessingConfig
from src.model.processing.VariedProcessingConfig import VariedProcessingConfig
from src.model.processing.Evaluation import Evaluation
from src.model.processing.Threshold import Threshold

import pandas as pd


class ProjectSnapshot(Project):
    __DEFAULT_PROCESSING_CONFIGS = [SimpleProcessingConfig(), VariedProcessingConfig()]
    __DEFAULT_THRESHOLDS = {}

    def __init__(self,
                 path: str,
                 previous: ProjectSnapshot = None,
                 next_: ProjectSnapshot = None,
                 model: Model = None,
                 processing_configs:
                 list[ProcessingConfig] = None,
                 selected_config_index: int = 0,
                 evaluation: Evaluation = None,
                 thresholds: dict[str, Threshold] = None):
        self.__path = path
        self.__previous: ProjectSnapshot | None = previous
        self.__next: ProjectSnapshot | None = next_
        self.__model: Model = model
        self.__processing_configs: list[ProcessingConfig] \
            = processing_configs if processing_configs is not None else ProjectSnapshot.__DEFAULT_PROCESSING_CONFIGS
        self.__selected_config_index: int = selected_config_index
        self.__evaluation: Evaluation | None = evaluation
        self.__thresholds: dict[str, Threshold] \
            = thresholds if thresholds is not None else ProjectSnapshot.__DEFAULT_THRESHOLDS

    @property
    def path(self) -> str:
        return self.__path

    def undo(self) -> Project:
        return self.__previous

    def redo(self) -> Project:
        return self.__next

    def get_selected_config_index(self) -> int:
        return self.__selected_config_index

    def set_selected_config_index(self, index: int):
        self.__selected_config_index = index

    def get_config_settings(self) -> list[dict[str, object]]:
        return list(map(lambda c: c.settings, self.__processing_configs))

    def set_config_settings(self, index: int, settings: dict[str, object]):
        self.__processing_configs[index] = self.__processing_configs[index].set_settings(settings)

    def get_config_display_names(self) -> list[str]:
        return list(map(lambda c: c.display_name, self.__processing_configs))

    def evaluate(self):
        self.__evaluation = self.__processing_configs[self.get_selected_config_index()].process(self.__model)

    def is_optimizable(self) -> bool:
        return self.__evaluation and self.__evaluation.is_optimizable

    def optimize_model(self):
        self.__model = self.__evaluation.optimize(self.__model)

    def get_raw_data(self, with_derivatives: bool = False) -> pd.DataFrame:
        return self.__model.data.raw_data.copy()

    def set_raw_data(self, data: pd.DataFrame):
        self.__model = self.__model.set_raw_data(data)

    def get_derivatives(self) -> dict[str, FunctionalExpression]:
        return self.__model.data.derivatives.copy()

    def set_derivative(self, label: str, function: FunctionalExpression):
        self.__model = self.__model.set_derivative(label, function)

    def remove_derivative(self, label: str):
        self.__model = self.__model.remove_derivative(label)

    def get_derivative_error_report(self, label: str) -> ErrorReport:
        return self.__model.get_derivative_error_report(label, {})  # TODO: USE SYSTEMATIC EVALUATION ALGOTITHM FOR ALL VARIABLES

    def get_alternatives(self) -> dict[str, FunctionalExpression]:
        return self.__model.alternatives.copy()

    def set_alternative(self, label: str, function: FunctionalExpression):
        self.__model = self.__model.set_alternative(label, function)

    def remove_alternative(self, label: str):
        self.__model = self.__model.remove_alternative(label)

    def get_alternative_error_report(self, label: str) -> ErrorReport:
        return self.__model.get_alternative_error_report(label, {})  # TODO: USE SYSTEMATIC EVALUATION ALGOTITHM FOR ALL VARIABLES

    def get_thresholds(self) -> dict[str, Threshold]:
        return self.__thresholds.copy()

    def set_thresholds(self, **thresholds: Threshold):
        self.__thresholds = thresholds.copy()

    def get_evaluation(self) -> pd.DataFrame:
        return self.__evaluation.result.copy()
