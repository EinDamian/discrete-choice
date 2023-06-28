from __future__ import annotations
from dataclasses import dataclass

from src.model.data.Data import Data
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport

import pandas as pd

@dataclass(frozen=True)
class Model:
    data: Data
    alternatives: dict[str, FunctionalExpression]

    def set_alternative(self, label: str, alternative: FunctionalExpression) -> Model:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def remove_alternative(self, label: str) -> Model:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_derivative(self, label: str, derivative: FunctionalExpression) -> Model:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def remove_derivative(self, label: str) -> Model:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_raw_data(self, raw_data: pd.DataFrame) -> Model:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_data(self, data: Data) -> Model:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_derivative_error_report(self, label: str, variables: dict[str, FunctionalExpression]) -> ErrorReport:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_alternative_error_report(self, label: str, variables: dict[str, FunctionalExpression]) -> ErrorReport:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
