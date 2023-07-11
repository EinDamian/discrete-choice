from __future__ import annotations
from dataclasses import dataclass

from src.model.data.Data import Data
from src.model.data.Alternative import Alternative
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport

import pandas as pd


@dataclass(frozen=True)
class Model:
    data: Data
    alternatives: dict[str, Alternative]
    choice: FunctionalExpression

    def set_alternative(self, label: str, alternative: Alternative) -> Model:
        new_alternatives = self.alternatives.copy()
        new_alternatives.update({label: alternative})
        return Model(self.data, new_alternatives, self.choice)

    def remove_alternative(self, label: str) -> Model:
        if label not in self.alternatives:
            raise KeyError(f'There is no alternative with the label {label}')

        new_alternatives = self.alternatives.copy()
        new_alternatives.pop(label)
        return Model(self.data, new_alternatives, self.choice)

    def set_derivative(self, label: str, derivative: FunctionalExpression) -> Model:
        return Model(self.data.set_derivative(label, derivative), self.alternatives, self.choice)

    def remove_derivative(self, label: str) -> Model:
        return Model(self.data.remove_derivative(label), self.alternatives, self.choice)

    def set_raw_data(self, raw_data: pd.DataFrame) -> Model:
        return Model(self.data.set_raw_data(raw_data), self.alternatives, self.choice)

    def set_data(self, data: Data) -> Model:
        return Model(data, self.alternatives, self.choice)

    def get_derivative_error_report(self, label: str, variables: dict[str, FunctionalExpression]) -> ErrorReport:
        return self.data.get_derivative_error_report(label, variables)

    def get_alternative_error_report(self, label: str, variables: dict[str, FunctionalExpression]) -> ErrorReport:
        if label not in self.alternatives:
            raise KeyError(f'There is no alternative with the label {label}')

        alternative_expression = self.alternatives.get(label).function
        return alternative_expression.get_error_report(**(variables | self.data.get_variables()))

    def set_choice(self, choice: FunctionalExpression) -> Model:
        return Model(self.data, self.alternatives, choice)