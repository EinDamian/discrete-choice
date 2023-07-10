"""This module contains only one class with the same name."""

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

    @staticmethod
    def __snapshot(version_offset: int = 0, new_snapshot: bool = False, move_current: bool = True):
        def __wrapper(func: Callable):
            def __do_operation(self, *args, **kwargs):
                p = self.__current_project
                remaining = version_offset

                while remaining < 0:
                    p = p.undo()
                    remaining += 1

                while remaining > 0:
                    p = p.redo()
                    remaining -= 1

                np = copy(p) if new_snapshot else p

                try:
                    ret = func(np, *args, **kwargs)
                except Exception as e:
                    raise e

                if new_snapshot:
                    np.__previous = p
                    np.__next = None
                    p.__next = np

                if move_current:
                    self.__current_project = np

                self.save()  # TODO: ASYNC
                return ret

            return __do_operation
        return __wrapper

    @property
    @__snapshot(0)
    def path(self: ProjectSnapshot) -> str:
        return self.path

    @__snapshot(-1)
    def undo(self: ProjectSnapshot) -> Project:
        return self

    @__snapshot(1)
    def redo(self: ProjectSnapshot) -> Project:
        return self

    @__snapshot(0)
    def get_selected_config_index(self: ProjectSnapshot) -> int:
        return self.get_selected_config_index()

    @__snapshot(1, new_snapshot=True)
    def set_selected_config_index(self: ProjectSnapshot, index: int):
        return self.set_selected_config_index(index)

    @__snapshot(0)
    def get_config_settings(self: ProjectSnapshot) -> list[dict[str, object]]:
        return self.get_config_settings()

    @__snapshot(1, new_snapshot=True)
    def set_config_settings(self: ProjectSnapshot, index: int, settings: dict[str, object]):
        return self.set_config_settings(index, settings)

    @__snapshot(0)
    def get_config_display_names(self: ProjectSnapshot) -> list[str]:
        return self.get_config_display_names()

    @__snapshot(1, new_snapshot=True)
    def evaluate(self: ProjectSnapshot):
        return self.evaluate()

    @__snapshot(0)
    def is_optimizable(self: ProjectSnapshot) -> bool:
        return self.is_optimizable()

    @__snapshot(1, new_snapshot=True)
    def optimize_model(self: ProjectSnapshot):
        return self.optimize_model()

    @__snapshot(0)
    def get_raw_data(self: ProjectSnapshot, with_derivatives: bool = False) -> pd.DataFrame:
        return self.get_raw_data(with_derivatives)

    @__snapshot(1, new_snapshot=True)
    def set_raw_data(self: ProjectSnapshot, data: pd.DataFrame):
        return self.set_raw_data(data)

    @__snapshot(0)
    def get_derivatives(self: ProjectSnapshot) -> dict[str, FunctionalExpression]:
        return self.get_derivatives()

    @__snapshot(1, new_snapshot=True)
    def set_derivative(self: ProjectSnapshot, label: str, function: FunctionalExpression):
        return self.set_derivative(label, function)

    @__snapshot(1, new_snapshot=True)
    def remove_derivative(self: ProjectSnapshot, label: str):
        return self.remove_derivative(label)

    @__snapshot(0)
    def get_derivative_error_report(self: ProjectSnapshot, label: str) -> ErrorReport:
        return self.get_derivative_error_report(label)

    @__snapshot(0)
    def get_alternatives(self: ProjectSnapshot) -> dict[str, FunctionalExpression]:
        return self.get_alternatives()

    @__snapshot(1, new_snapshot=True)
    def set_alternative(self: ProjectSnapshot, label: str, function: FunctionalExpression):
        return self.set_alternative(label, function)

    @__snapshot(1, new_snapshot=True)
    def remove_alternative(self: ProjectSnapshot, label: str):
        return self.remove_alternative(label)

    def get_alternative_error_report(self, label: str) -> ErrorReport:
        return self.__current_project.get_alternative_error_report(label)

    def get_thresholds(self) -> dict[str, Threshold]:
        return self.__current_project.get_thresholds()

    @__snapshot(1, new_snapshot=True)
    def set_thresholds(self: ProjectSnapshot, **thresholds: Threshold):
        return self.set_thresholds(**thresholds)

    @__snapshot(0)
    def get_evaluation(self: ProjectSnapshot) -> pd.DataFrame:
        return self.get_evaluation()
