from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property

from functions.FunctionalExpression import FunctionalExpression
from functions.ErrorReport import ErrorReport

import pandas as pd

@dataclass(frozen=True)
class Data:
    raw_data: pd.DataFrame
    derivatives: dict[str, FunctionalExpression]

    @cached_property
    def complete_data(self) -> pd.DataFrame:
        # TODO: Idee: https://www.geeksforgeeks.org/create-a-new-column-in-pandas-dataframe-based-on-the-existing-columns/
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_raw_data(self, raw_data: pd.DataFrame) -> Data:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_derivative(self, label: str, derivative: dict[str, FunctionalExpression]) -> Data:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def remove_derivative(self, label: str) -> Data:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_derivative_error_report(self, label: str, variables: dict[str, FunctionalExpression]) -> ErrorReport:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
