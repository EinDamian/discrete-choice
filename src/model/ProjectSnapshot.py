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

    def get_raw_data_path(self) -> str:
        return self.__model.data.raw_data_path

    def set_raw_data(self, data: pd.DataFrame, path: str | None):
        self.__model = self.__model.set_raw_data(data, path)

    def get_derivatives(self) -> dict[str, FunctionalExpression]:
        return self.__model.data.derivatives.copy()

    def set_derivatives(self, **functions: FunctionalExpression):
        self.__model = self.__model.set_derivative(**functions)

    def remove_derivatives(self, *label: str):
        self.__model = self.__model.remove_derivative(*label)

    def get_derivative_error_report(self, label: str) -> ErrorReport:
        return self.__model.get_derivative_error_report(label, ProjectSnapshot.__eval_derivatives(self.__model))

    def get_derivative_type(self, label: str) -> type:
        return self.__model.data.derivatives[label].type(**ProjectSnapshot.__eval_derivatives(self.__model))

    @staticmethod
    def __eval_derivatives(model: Model, check: bool = True) -> dict[str, object]:
        raw_data = {label: model.data.raw_data[label].iloc[0] for label in model.data.raw_data}
        derivative_depends = {label: expr.variables for label, expr in model.data.derivatives.items()}

        variables = raw_data
        for label in TopologicalSorter(derivative_depends).static_order():
            if label not in variables and label in model.data.derivatives:
                expr = model.data.derivatives[label]

                if not check or expr.get_error_report(**variables).valid:
                    variables[label] = expr.eval(**variables)

        return variables

    def get_derivative_free_variables(self) -> set[str]:
        raw_data = {label: self.__model.data.raw_data[label].iloc[0] for label in self.__model.data.raw_data}
        derivative_depends = {label: expr.variables for label, expr in self.__model.data.derivatives.items()}
        return functools.reduce(lambda a, b: a | b,
                                derivative_depends.values(), set()) - derivative_depends.keys() - raw_data.keys()

    def get_alternatives(self) -> dict[str, Alternative]:
        return self.__model.alternatives.copy()

    def set_alternatives(self, **alternatives: Alternative):
        self.__model = self.__model.set_alternative(**alternatives)

    def remove_alternatives(self, *label: str):
        self.__model = self.__model.remove_alternative(*label)

    def get_alternative_error_report(self, label: str) -> ErrorReport:
        derivatives = ProjectSnapshot.__eval_derivatives(self.__model)
        derivative_depends = {label: expr.variables for label, expr in self.__model.data.derivatives.items()}
        alternatives = ProjectSnapshot.__eval_alternatives(self.__model, derivatives=derivatives)
        alternative_depends = {label: alt.function.variables for label, alt in self.__model.alternatives.items()}
        def_depends = derivative_depends | alternative_depends
        beta_labels = functools.reduce(lambda a, b: a | b,
                                       alternative_depends.values(), set()) - def_depends.keys() - derivatives.keys()
        betas = {label: 1 for label in beta_labels}
        return self.__model.get_alternative_error_report(label, derivatives | alternatives | betas)

    @staticmethod
    def __eval_alternatives(model: Model, check: bool = True, derivatives: dict[str, object] = None) -> dict[str, object]:
        derivatives = ProjectSnapshot.__eval_derivatives(model, check) if derivatives is None else derivatives
        derivative_depends = {label: expr.variables for label, expr in model.data.derivatives.items()}
        alternative_depends = {label: alt.function.variables for label, alt in model.alternatives.items()}
        def_depends = derivative_depends | alternative_depends
        beta_labels = functools.reduce(lambda a, b: a | b,
                                       alternative_depends.values(), set()) - def_depends.keys() - derivatives.keys()
        betas = {label: 1 for label in beta_labels}

        variables = {}
        params = derivatives | betas
        for label in TopologicalSorter(alternative_depends).static_order():
            if label in model.alternatives:
                expr = model.alternatives[label].function

                if not check or expr.get_error_report(**(params | variables)).valid:
                    variables[label] = expr.eval(**(params | variables))

        return variables

    def get_availability_condition_error_report(self, label: str) -> ErrorReport:
        return self.__model.get_availability_condition_error_report(
            label, ProjectSnapshot.__eval_derivatives(self.__model) | ProjectSnapshot.__eval_alternatives(self.__model))

    def get_choice(self) -> FunctionalExpression:
        return self.__model.choice

    def set_choice(self, choice: FunctionalExpression):
        self.__model = self.__model.set_choice(choice)

    def get_thresholds(self) -> dict[str, Threshold]:
        return self.__thresholds.copy()

    def set_thresholds(self, **thresholds: Threshold):
        self.__thresholds = thresholds.copy()

    def get_evaluation(self) -> pd.DataFrame | None:
        return self.__evaluation.result.copy() if self.__evaluation is not None else None
