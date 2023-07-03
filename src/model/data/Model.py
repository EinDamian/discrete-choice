from __future__ import annotations
from dataclasses import dataclass

from src.model.data.Data import Data
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport

import pandas as pd


@dataclass(frozen=True)
class Model:
    _data: Data
    _alternatives: dict[str, FunctionalExpression]

    def set_alternative(self, label: str, alternative: FunctionalExpression) -> Model:
        new_alternatives = self._alternatives.copy()
        new_alternatives.update({label: alternative})
        return Model(self._data, new_alternatives)

    def remove_alternative(self, label: str) -> Model:
        if label not in self._alternatives:
            raise KeyError('There is no alternative with the label {}'.format(label))

        new_alternatives = self._alternatives.copy()
        new_alternatives.pop(label)
        return Model(self._data, new_alternatives)

    def set_derivative(self, label: str, derivative: FunctionalExpression) -> Model:
        return Model(self._data.set_derivative(label, derivative), self._alternatives)

    def remove_derivative(self, label: str) -> Model:
        return Model(self._data.remove_derivative(label), self._alternatives)

    def set_raw_data(self, raw_data: pd.DataFrame) -> Model:
        return Model(self._data.set_raw_data(raw_data), self._alternatives)

    def set_data(self, data: Data) -> Model:
        return Model(data, self._alternatives)

    def get_derivative_error_report(self, label: str, variables: dict[str, FunctionalExpression]) -> ErrorReport:
        return self._data.get_derivative_error_report(label, variables)

    def get_alternative_error_report(self, label: str, variables: dict[str, FunctionalExpression]) -> ErrorReport:
        if label not in self._alternatives:
            raise KeyError('There is no alternative with the label {}'.format(label))

        alternative_expression = self._alternatives.get(label)
        return alternative_expression.get_error_report(variables)