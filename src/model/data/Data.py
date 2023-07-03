from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property

from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport

import pandas as pd

@dataclass(frozen=True)
class Data:
    _raw_data: pd.DataFrame
    _derivatives: dict[str, FunctionalExpression]

    @cached_property
    def complete_data(self) -> pd.DataFrame:
        complete_data = self._raw_data.copy(True)
        for key in self._derivatives.keys():
            derivative_expr = self._derivatives.get(key)
            if derivative_expr.get_error_report().is_valid():
                # TODO: add current row values to variables -> generic column function not possible?
                complete_data[key] = derivative_expr.eval(**self._derivatives)
        return complete_data

    def set_raw_data(self, raw_data: pd.DataFrame) -> Data:
        return Data(raw_data, self._derivatives)

    def set_derivative(self, label: str, derivative: FunctionalExpression) -> Data:
        new_derivatives = self._derivatives.copy()
        new_derivatives.update({label: derivative})
        return Data(self._raw_data, new_derivatives)

    def remove_derivative(self, label: str) -> Data:
        if label not in self._derivatives:
            raise KeyError('There is no derivative with the label {}'.format(label))

        new_derivatives = self._derivatives.copy()
        new_derivatives.pop(label)
        return Data(self._raw_data, new_derivatives)

    def get_derivative_error_report(self, label: str, variables: dict[str, FunctionalExpression]) -> ErrorReport:
        if label not in self._derivatives:
            raise KeyError('There is no derivative with the label {}'.format(label))

        derivative_expression = self._derivatives.get(label)
        return derivative_expression.get_error_report(**variables)
