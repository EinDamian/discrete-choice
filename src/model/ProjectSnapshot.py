from __future__ import annotations
from copy import copy
import json

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
                 next: ProjectSnapshot = None,
                 model: Model = None,
                 processing_configs:
                 list[ProcessingConfig] = None,
                 selected_config_index: int = 0,
                 evaluation: Evaluation = None,
                 thresholds: dict[str, Threshold] = None):
        self.__path = path
        self.__previous: ProjectSnapshot | None = previous
        self.__next: ProjectSnapshot | None = next
        self.__model: Model = model
        self.__processing_configs: list[ProcessingConfig] = processing_configs if processing_configs is not None else ProjectSnapshot.__DEFAULT_PROCESSING_CONFIGS
        self.__selected_config_index: int = selected_config_index
        self.__evaluation: Evaluation | None = evaluation
        self.__thresholds: dict[str, Threshold] = thresholds if thresholds is not None else ProjectSnapshot.__DEFAULT_THRESHOLDS

    @property
    def path(self) -> str:
        return self.__path

    def save(self, path: str = None):
        path = path if path is not None else self.path
        snap = copy(self)
        del snap.__path  # do not save path through redundancy (already given through file location)
        del snap.__previous, snap.__next  # do not save previous and next versions

        with open(path, 'w') as f:
            f.write(json.dumps(snap))

    def undo(self) -> Project:
        return self.__previous

    def redo(self) -> Project:
        return self.__next

    @property
    def selected_config_index(self) -> int:
        return self.__selected_config_index

    @selected_config_index.setter
    def selected_config_index(self, index: int):
        self.__selected_config_index = index

    @property
    def config_settings(self) -> list[pd.DataFrame]:
        return list(map(lambda c: c.settings, self.__processing_configs))

    def set_config_settings(self, index: int, settings: pd.DataFrame):
        self.__processing_configs[index] = self.__processing_configs[index].set_settings(settings)

    @property
    def config_display_names(self) -> list[str]:
        return list(map(lambda c: c.display_name, self.__processing_configs))

    def evaluate(self):
        self.__evaluation = self.__processing_configs[self.selected_config_index].process(self.__model)

    @property
    def is_optimizable(self) -> bool:
        return self.__evaluation and self.__evaluation.is_optimizable

    def optimize_model(self):
        self.__model = self.__evaluation.optimize(self.__model)

    def get_raw_data(self, with_derivatives: bool = False) -> pd.DataFrame:
        return self.__model.data.raw_data.copy()

    def set_raw_data(self, data: pd.DataFrame):
        self.__model = self.__model.set_raw_data(data)

    @property
    def derivatives(self) -> dict[str, FunctionalExpression]:
        return self.__model.data.derivatives.copy()

    def set_derivative(self, label: str, function: FunctionalExpression):
        self.__model = self.__model.set_derivative(label, function)

    def remove_derivative(self, label: str):
        self.__model = self.__model.remove_derivative(label)

    def import_derivative(self, path: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def export_derivative(self, label: str, path: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_derivative_error_report(self, label: str) -> ErrorReport:
        return self.__model.get_derivative_error_report(label, {})  # TODO: BERÜCKSICHTIGUNG VON VARIABLEN

    @property
    def alternatives(self) -> dict[str, FunctionalExpression]:
        return self.__model.alternatives.copy()

    def set_alternative(self, label: str, function: FunctionalExpression):
        self.__model = self.__model.set_alternative(label, function)

    def remove_alternative(self, label: str):
        self.__model = self.__model.remove_alternative(label)

    def import_alternative(self, path: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def export_alternative(self, label: str, path: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_alternative_error_report(self, label: str) -> ErrorReport:
        return self.__model.get_alternative_error_report(label, {})  # TODO: BERÜCKSICHTIGUNG VON VARIABLEN

    @property
    def thresholds(self) -> dict[str, Threshold]:
        return self.__thresholds.copy()

    @thresholds.setter
    def thresholds(self, **thresholds: Threshold):
        self.__thresholds = thresholds.copy()

    @property
    def evaluation(self) -> pd.DataFrame:
        return self.__evaluation.result.copy()
