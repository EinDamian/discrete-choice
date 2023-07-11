from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property

from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport

import pandas as pd
from graphlib import TopologicalSorter


@dataclass(frozen=True)
class Data:
    raw_data: pd.DataFrame
    derivatives: dict[str, FunctionalExpression]

    def get_sorted_derivatives(self):
        graph = {}
        variables = self.derivatives.copy()

        for col in self.raw_data.columns:
            variables[str(col)] = self.raw_data[col].iloc[0]

        for key in self.derivatives.keys():
            expression = self.derivatives.get(key)
            # TODO: remove print
            print(key + " errors: " + str(expression.get_error_report(**variables).marker))
            if expression.get_error_report(**variables).valid:
                graph[key] = expression.variables
        sorter = TopologicalSorter(graph)  # acyclic because only valid expressions
        sorted_variables = list(sorter.static_order())
        # filter for only derivatives
        return [x for x in sorted_variables if x in self.derivatives]

    @cached_property
    def complete_data(self) -> pd.DataFrame:
        complete_data = self.raw_data.copy(True)

        # add derivatives
        for key in self.get_sorted_derivatives():
            expression = self.derivatives.get(key)
            row_value_dict = complete_data.to_dict(orient='index')
            complete_data[key] = complete_data.index.map(row_value_dict)
            complete_data[key] = complete_data[key].apply(lambda x: expression.eval(**x))
        return complete_data

    def set_raw_data(self, raw_data: pd.DataFrame) -> Data:
        return Data(raw_data, self.derivatives)

    def set_derivative(self, label: str, derivative: FunctionalExpression) -> Data:
        new_derivatives = self.derivatives.copy()
        new_derivatives.update({label: derivative})
        return Data(self.raw_data, new_derivatives)

    def remove_derivative(self, label: str) -> Data:
        if label not in self.derivatives:
            raise KeyError('There is no derivative with the label {}'.format(label))

        new_derivatives = self.derivatives.copy()
        new_derivatives.pop(label)
        return Data(self.raw_data, new_derivatives)

    def get_derivative_error_report(self, label: str, variables: dict[str, FunctionalExpression]) -> ErrorReport:
        if label not in self.derivatives:
            raise KeyError('There is no derivative with the label {}'.format(label))

        derivative_expression = self.derivatives.get(label)
        return derivative_expression.get_error_report(**variables)
