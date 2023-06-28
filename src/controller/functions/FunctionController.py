from __future__ import annotations

from ...model.data.functions.FunctionalExpression import FunctionalExpression
from ..FileManager import FileManager
from ..AbstractController import AbstractController

class FunctionController(FileManager, AbstractController):
    """Class that is used to control the different types of funtions."""

    def add(self, function: FunctionalExpression):
        raise NotImplementedError

    def remove(self, label: str):
        raise NotImplementedError

    def change(self, label: str, function: FunctionalExpression):
        raise NotImplementedError

    def validate(self, function: FunctionalExpression):
        raise NotImplementedError

    def get_error_report(self, label: str):
        raise NotImplementedError
