from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property

from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport

import pandas as pd
from graphlib import TopologicalSorter


@dataclass(frozen=True)
class Data:
    """
    Maintains input data and all derivatives. Represents a current Snapshot of this data.

    Attributes:
        raw_data: Input data on which calculations are based on.
        derivatives: All derivatives in the current model.
    """
    raw_data: pd.DataFrame
    derivatives: dict[str, FunctionalExpression]

    def get_sorted_derivatives(self):
        """
        Sort valid derivatives by dependencies to each other.
        :return: Sorted derivatives. First to last represents evaluable order.
        """
        graph = {}
        variables = self.get_variables()

        for key in self.derivatives.keys():
            expression = self.derivatives.get(key)
            # TODO: remove print
            print(key + " errors: " + str(expression.get_error_report(**variables).marker))
            if expression.get_error_report(**variables).valid:
                graph[key] = expression.variables
        sorter = TopologicalSorter(graph)  # acyclic because only valid expressions
        sorted_variables = list(sorter.static_order())
        # filter for only derivatives so eval can be called on all elements
        # TODO: might be irrelevant if get_variables only returns FunctionalExpressions for values
        return [x for x in sorted_variables if x in self.derivatives]

    @cached_property
    def complete_data(self) -> pd.DataFrame:
        """
        Create a new table containing the raw data and calculated columns for all valid derivatives.
        :return: New table with raw data and calculated valid derivatives.
        """
        complete_data = self.raw_data.copy(True)

        # add derivatives
        for key in self.get_sorted_derivatives():
            expression = self.derivatives.get(key)
            row_value_dict = complete_data.to_dict(orient='index')
            complete_data[key] = complete_data.index.map(row_value_dict)
            complete_data[key] = complete_data[key].apply(lambda x: expression.eval(**x))
        return complete_data

    def set_raw_data(self, raw_data: pd.DataFrame) -> Data:
        """
        Set the raw data. Further calculations are based on this data.
        :param raw_data: Input data.
        :return: Copy of the Data object with the data.
        """
        return Data(raw_data, self.derivatives)

    def set_derivative(self, label: str, derivative: FunctionalExpression) -> Data:
        """
        Add or change the function of a derivative.
        :param label: Name of the derivative.
        :param derivative: Function of the derivative.
        :return: Copy of the Data object with the new derivative.
        """
        new_derivatives = self.derivatives.copy()
        new_derivatives.update({label: derivative})
        return Data(self.raw_data, new_derivatives)

    def remove_derivative(self, label: str) -> Data:
        """
        Remove an existing derivative.
        :param label: Name of the derivative.
        :return: Copy of the Data object without the derivative.
        :raises KeyError: No derivative with this label exists.
        """
        if label not in self.derivatives:
            raise KeyError(f'There is no derivative with the label {label}')

        new_derivatives = self.derivatives.copy()
        new_derivatives.pop(label)
        return Data(self.raw_data, new_derivatives)

    def get_variables(self):
        """
        Get all derivatives and attributes of the raw data.
        :return: Union of derivatives and raw data attributes.
        """
        variables = dict()
        # TODO: test if a row even exists
        # TODO: turn values into FunctionalExpressions?
        for col in self.raw_data.columns:
            variables[str(col)] = self.raw_data[col].iloc[0]
        variables |= self.derivatives.copy()
        return variables

    def get_derivative_error_report(self, label: str, variables: dict[str, FunctionalExpression]) -> ErrorReport:
        """
        Get an error report of the derivative. Contains all found errors.
        :param label: Name of the derivative.
        :param variables: Additional variables usable in the derivative.
        :return: Error report containing all found errors.
        :raises KeyError: No derivative with this label exists.
        """
        if label not in self.derivatives:
            raise KeyError(f'There is no derivative with the label {label}')

        derivative_expression = self.derivatives.get(label)
        return derivative_expression.get_error_report(**(variables | self.get_variables()))
