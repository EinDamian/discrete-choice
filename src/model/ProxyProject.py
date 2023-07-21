"""This module contains only one class with the same name."""

from __future__ import annotations
from typing import Callable
from copy import copy

from src.model.Project import Project
from src.model.ProjectSnapshot import ProjectSnapshot
from src.model.SnapshotError import SnapshotError
from src.model.data.Alternative import Alternative
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport
from src.model.processing.Threshold import Threshold

import pandas as pd


class ProxyProject(Project):
    def __init__(self, project: ProjectSnapshot = None):
        self.__current_project: ProjectSnapshot = project if project is not None else ProjectSnapshot()

    @staticmethod
    def __snapshot(version_offset: int = 0, new_snapshot: bool = False, move_current: bool = True):
        def __wrapper(func: Callable):
            def __do_operation(self, *args, **kwargs):
                p = self.__current_project
                remaining = version_offset

                while remaining < 0:
                    prev = p.undo()
                    p = prev if prev is not None else p
                    remaining += 1

                while remaining > 0:
                    next_ = p.redo()
                    p = next_ if next_ is not None else p
                    remaining -= 1

                np = copy(p) if new_snapshot else p

                try:
                    ret = func(np, *args, **kwargs)
                except Exception as e:
                    raise SnapshotError(parent=e) from e

                if new_snapshot:
                    np.previous = p
                    np.next = None
                    p.next = np

                if move_current:
                    self.__current_project = np

                return ret

            return __do_operation
        return __wrapper

    @property
    @__snapshot()
    def path(self: ProjectSnapshot) -> str:
        return self.path

    @__snapshot()
    def set_path(self: ProjectSnapshot, path: str):
        return self.set_path(path)

    @__snapshot(-1)
    def undo(self: ProjectSnapshot) -> Project:
        pass

    def can_undo(self) -> bool:
        """
        :return: Truth value, if the UNDO-Operation is available.
        :rtype: bool
        """
        return self.__current_project.previous is not None

    @__snapshot(1)
    def redo(self: ProjectSnapshot) -> Project:
        pass

    def can_redo(self) -> bool:
        """
        :return: Truth value, if the REDO-Operation is available.
        :rtype: bool
        """
        return self.__current_project.next is not None

    @__snapshot()
    def get_selected_config_index(self: ProjectSnapshot) -> int:
        return self.get_selected_config_index()

    @__snapshot(new_snapshot=True)
    def set_selected_config_index(self: ProjectSnapshot, index: int):
        return self.set_selected_config_index(index)

    @__snapshot()
    def get_config_settings(self: ProjectSnapshot) -> list[dict[str, object]]:
        return self.get_config_settings()

    @__snapshot(new_snapshot=True)
    def set_config_settings(self: ProjectSnapshot, index: int, settings: dict[str, object]):
        return self.set_config_settings(index, settings)

    @__snapshot()
    def get_config_display_names(self: ProjectSnapshot) -> list[str]:
        return self.get_config_display_names()

    @__snapshot(new_snapshot=True)
    def evaluate(self: ProjectSnapshot):
        return self.evaluate()

    @__snapshot()
    def is_optimizable(self: ProjectSnapshot) -> bool:
        return self.is_optimizable()

    @__snapshot(new_snapshot=True)
    def optimize_model(self: ProjectSnapshot):
        return self.optimize_model()

    @__snapshot()
    def get_raw_data(self: ProjectSnapshot, with_derivatives: bool = False) -> pd.DataFrame:
        return self.get_raw_data(with_derivatives)

    @__snapshot()
    def get_raw_data_path(self: ProjectSnapshot) -> str:
        return self.get_raw_data_path()

    @__snapshot(new_snapshot=True)
    def set_raw_data(self: ProjectSnapshot, data: pd.DataFrame, path: str | None):
        return self.set_raw_data(data, path)

    @__snapshot()
    def get_derivatives(self: ProjectSnapshot) -> dict[str, FunctionalExpression]:
        return self.get_derivatives()

    @__snapshot(new_snapshot=True)
    def set_derivatives(self: ProjectSnapshot, **derivatives: FunctionalExpression):
        return self.set_derivatives(**derivatives)

    @__snapshot(new_snapshot=True)
    def remove_derivatives(self: ProjectSnapshot, *label: str):
        return self.remove_derivatives(*label)

    @__snapshot()
    def get_derivative_error_report(self: ProjectSnapshot, label: str) -> ErrorReport:
        return self.get_derivative_error_report(label)

    @__snapshot()
    def get_derivative_type(self: ProjectSnapshot, label: str) -> type:
        return self.get_derivative_type(label)

    @__snapshot()
    def get_derivative_free_variables(self: ProjectSnapshot) -> set[str]:
        return self.get_derivative_free_variables()

    @__snapshot()
    def get_alternatives(self: ProjectSnapshot) -> dict[str, Alternative]:
        return self.get_alternatives()

    @__snapshot(new_snapshot=True)
    def set_alternatives(self: ProjectSnapshot, **alternatives: Alternative):
        return self.set_alternatives(**alternatives)

    @__snapshot(new_snapshot=True)
    def remove_alternatives(self: ProjectSnapshot, *label: str):
        return self.remove_alternatives(*label)

    @__snapshot()
    def get_alternative_error_report(self: ProjectSnapshot, label: str) -> ErrorReport:
        return self.get_alternative_error_report(label)

    @__snapshot()
    def get_availability_condition_error_report(self: ProjectSnapshot, label: str) -> ErrorReport:
        return self.get_availability_condition_error_report(label)

    @__snapshot()
    def get_choice(self: ProjectSnapshot) -> FunctionalExpression:
        return self.get_choice()

    @__snapshot(new_snapshot=True)
    def set_choice(self: ProjectSnapshot, choice: FunctionalExpression):
        return self.set_choice(choice)

    @__snapshot()
    def get_thresholds(self: ProjectSnapshot) -> dict[str, Threshold]:
        return self.get_thresholds()

    @__snapshot(new_snapshot=True)
    def set_thresholds(self: ProjectSnapshot, **thresholds: Threshold):
        return self.set_thresholds(**thresholds)

    @__snapshot()
    def get_evaluation(self: ProjectSnapshot) -> pd.DataFrame | None:
        return self.get_evaluation()
