from __future__ import annotations
from typing import Callable
from copy import copy

from src.model.Project import Project
from src.model.ProjectSnapshot import ProjectSnapshot
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport
from src.model.processing.Threshold import Threshold

import pandas as pd


class ProxyProject(Project):
    def __init__(self, project: ProjectSnapshot):
        self.__current_project: ProjectSnapshot = project

    def __do_operation(self, operation: Callable[[ProjectSnapshot], bool]):
        p = self.__current_project
        cp = copy(p)
        success = operation(cp)

        if success:
            cp.previous = p
            p.next = cp
            self.__current_project = cp
            self.save()  # TODO: ASYNC

    @property
    def path(self) -> str:
        return self.__current_project.path

    def save(self, path: str = None):
        self.__current_project.save(path)

    def undo(self) -> Project:
        self.__current_project = self.__current_project.undo()
        return self

    def redo(self) -> Project:
        self.__current_project =  self.__current_project.redo()
        return self

    @property
    def selected_config_index(self) -> int:
        return self.__current_project.selected_config_index

    @selected_config_index.setter
    def selected_config_index(self, index: int):
        def op(p: ProjectSnapshot):
            p.selected_config_index = index
            return True

        self.__do_operation(op)

    @property
    def config_settings(self) -> list[pd.DataFrame]:
        return self.__current_project.config_settings

    def set_config_settings(self, index: int, settings: pd.DataFrame):
        def op(p: ProjectSnapshot):
            p.set_config_settings(index, settings)
            return True

        self.__do_operation(op)

    @property
    def config_display_names(self) -> list[str]:
        return self.__current_project.config_display_names

    def evaluate(self):
        return self.__current_project.evaluate()

    @property
    def is_optimizable(self) -> bool:
        return self.__current_project.is_optimizable

    def optimize_model(self):
        return self.__current_project.optimize_model()

    def get_raw_data(self, with_derivatives: bool = False) -> pd.DataFrame:
        return self.__current_project.get_raw_data(with_derivatives)

    def set_raw_data(self, data: pd.DataFrame):
        return self.__current_project.set_raw_data(data)

    @property
    def derivatives(self) -> dict[str, FunctionalExpression]:
        return self.__current_project.derivatives

    def set_derivative(self, label: str, function: FunctionalExpression):
        def op(p: ProjectSnapshot):
            p.set_derivative(label, function)
            return True

        self.__do_operation(op)

    def remove_derivative(self, label: str):
        def op(p: ProjectSnapshot):
            p.remove_derivative(label)
            return True

        self.__do_operation(op)

    def import_derivative(self, path: str):
        def op(p: ProjectSnapshot):
            p.import_derivative(path)
            return True

        self.__do_operation(op)

    def export_derivative(self, label: str, path: str):
        def op(p: ProjectSnapshot):
            p.export_derivative(label, path)
            return True

        self.__do_operation(op)

    def get_derivative_error_report(self, label: str) -> ErrorReport:
        return self.__current_project.get_derivative_error_report(label)

    @property
    def alternatives(self) -> dict[str, FunctionalExpression]:
        return self.__current_project.alternatives

    def set_alternative(self, label: str, function: FunctionalExpression):
        def op(p: ProjectSnapshot):
            p.set_alternative(label, function)
            return True

        self.__do_operation(op)

    def remove_alternative(self, label: str):
        def op(p: ProjectSnapshot):
            p.remove_alternative(label)
            return True

        self.__do_operation(op)

    def import_alternative(self, path: str):
        def op(p: ProjectSnapshot):
            p.import_alternative(path)
            return True

        self.__do_operation(op)

    def export_alternative(self, label: str, path: str):
        def op(p: ProjectSnapshot):
            p.export_alternative(label, path)
            return True

        self.__do_operation(op)

    def get_alternative_error_report(self, label: str) -> ErrorReport:
        return self.__current_project.get_alternative_error_report(label)

    @property
    def thresholds(self) -> dict[str, Threshold]:
        return self.__current_project.thresholds

    @thresholds.setter
    def thresholds(self, **thresholds: Threshold):
        def op(p: ProjectSnapshot):
            p.thresholds = thresholds
            return True

        self.__do_operation(op)

    @property
    def evaluation(self) -> pd.DataFrame:
        return self.__current_project.evaluation
