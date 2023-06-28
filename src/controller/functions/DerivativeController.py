from __future__ import annotations

from ...model.data.functions.FunctionalExpression import FunctionalExpression
from FunctionController import FunctionController

class DerivativeController(FunctionController):
    """Controller used to control all changes regarding the derivatives"""

    def get_derivatives(self) -> dict[str, FunctionalExpression]:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def add(self, function: FunctionalExpression):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def remove(self, label: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def change(self, label: str, function: FunctionalExpression):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def validate(self, function: FunctionalExpression):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_error_report(self, label: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
