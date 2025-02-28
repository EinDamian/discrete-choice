"""This module contains only one class with the same name."""

from __future__ import annotations
from graphlib import TopologicalSorter
import functools

from src.model.Project import Project
from src.model.data.Model import Model
from src.model.data.Data import Data
from src.model.data.Alternative import Alternative
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport
from src.model.processing.ProcessingConfig import ProcessingConfig
from src.model.processing.SingleLogitBiogemeConfig import SingleLogitBiogemeConfig
from src.model.processing.VariedLogitBiogemeConfig import VariedLogitBiogemeConfig
from src.model.processing.Evaluation import Evaluation
from src.model.processing.Threshold import Threshold

import pandas as pd


class ProjectSnapshot(Project):
    __DEFAULT_PROCESSING_CONFIGS = [SingleLogitBiogemeConfig(), VariedLogitBiogemeConfig()]
    __DEFAULT_THRESHOLDS = {}

    def __init__(self,
                 path: str = None,
                 previous: ProjectSnapshot = None,
                 next_: ProjectSnapshot = None,
                 model: Model = Model(Data(pd.DataFrame(), None, {}), {}, FunctionalExpression('')),
                 processing_configs: list[ProcessingConfig] = None,
                 selected_config_index: int = 0,
                 evaluation: Evaluation = None,
                 thresholds: dict[str, Threshold] = None):
        self.__path = path
        self.previous: ProjectSnapshot | None = previous
        self.next: ProjectSnapshot | None = next_
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

    def set_path(self, path: str):
        self.__path = path

    def undo(self) -> Project:
        return self.previous

    def redo(self) -> Project:
        return self.next

    def get_selected_config_index(self) -> int:
        return self.__selected_config_index

    def set_selected_config_index(self, index: int):
        self.__selected_config_index = index

    def get_config_settings(self) -> list[dict[str, object]]:
        return list(map(lambda c: c.settings, self.__processing_configs))

    def set_config_settings(self, index: int, settings: dict[str, FunctionalExpression]):
        self.__processing_configs = self.__processing_configs.copy()
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
        if with_derivatives:
            return self.__model.data.complete_data
        return self.__model.data.raw_data.copy()

    def get_raw_data_path(self) -> str:
        return self.__model.data.raw_data_path

    def set_raw_data(self, data: pd.DataFrame, path: str | None):
        self.__model = self.__model.set_raw_data(data, path)

    def get_derivatives(self) -> dict[str, FunctionalExpression]:
        return self.__model.data.derivatives.copy()

    def set_derivatives(self, **derivatives: FunctionalExpression):
        for label, function in derivatives.items():
            self.__model = self.__model.set_derivative(label, function)

    def remove_derivatives(self, *label: str):
        for la in label:
            self.__model = self.__model.remove_derivative(la)

    def get_derivative_error_report(self, label: str) -> ErrorReport:
        config = self.__processing_configs[self.__selected_config_index]
        return self.__model.get_derivative_error_report(label, config.settings)

    def get_derivative_type(self, label: str) -> type:
        config = self.__processing_configs[self.__selected_config_index]
        return self.__model.get_derivative_type(label, config.settings)

    def get_derivative_free_variables(self) -> set[str]:
        # collect dependencies of derivatives
        derivative_depends = {label: expr.variables for label, expr in self.__model.data.derivatives.items()}

        # calculate free variables in derivatives
        defined_labels = self.__model.data.get_variables().keys()
        used_labels = functools.reduce(lambda a, b: a | b, derivative_depends.values(), set())
        free_labels = used_labels - defined_labels

        return free_labels

    def get_alternatives(self) -> dict[str, Alternative]:
        return self.__model.alternatives.copy()

    def set_alternatives(self, **alternatives: Alternative):
        for label, alt in alternatives.items():
            self.__model = self.__model.set_alternative(label, alt)

    def remove_alternatives(self, *label: str):
        for la in label:
            self.__model = self.__model.remove_alternative(la)

    def get_alternative_error_report(self, label: str) -> ErrorReport:
        config = self.__processing_configs[self.__selected_config_index]

        # collect dependencies of alternatives
        alternative_depends = {label: alt.function.variables for label, alt in self.__model.alternatives.items()}

        # calculate free variables in alternatives
        defined_labels = self.__model.get_variables().keys()
        used_labels = functools.reduce(lambda a, b: a | b, alternative_depends.values(), set())
        free_labels = used_labels - defined_labels

        # free labels in alternatives are treated as beta variables
        # set all beta variables to 1 to get a representative error report
        betas = {label: 1 for label in free_labels}

        return self.__model.get_alternative_error_report(label, config.settings | betas)

    def get_availability_condition_error_report(self, label: str) -> ErrorReport:
        config = self.__processing_configs[self.__selected_config_index]
        return self.__model.get_availability_condition_error_report(label, config.settings)

    def get_choice(self) -> FunctionalExpression:
        return self.__model.choice

    def set_choice(self, choice: FunctionalExpression):
        self.__model = self.__model.set_choice(choice)

    def get_choice_error_report(self) -> ErrorReport:
        return self.get_choice().get_error_report(**self.__model.data.get_variables())

    def get_thresholds(self) -> dict[str, Threshold]:
        return self.__thresholds.copy()

    def set_thresholds(self, **thresholds: Threshold):
        self.__thresholds = thresholds.copy()

    def get_evaluation(self) -> pd.DataFrame | None:
        return self.__evaluation.result.copy() if self.__evaluation is not None else None
