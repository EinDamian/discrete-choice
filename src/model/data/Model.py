from __future__ import annotations
from dataclasses import dataclass

from src.model.data.Data import Data
from src.model.data.Alternative import Alternative
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport

import pandas as pd


@dataclass(frozen=True)
class Model:
    """
    Maintains input data, all alternatives and all derivatives. Represents a current Snapshot of this data.

    Attributes:
        data: Data object maintaining derivatives and input data.
        alternatives: All alternatives in the current model.
        choice: Choice function of the model.
    """
    data: Data
    alternatives: dict[str, Alternative]
    choice: FunctionalExpression

    def set_alternative(self, label: str, alternative: Alternative) -> Model:
        """
        Add or change the function of an alternative.
        :param label: Name of the alternative.
        :param alternative: Function of the alternative.
        :return: Copy of the Model object with the new alternative.
        """
        new_alternatives = self.alternatives.copy()
        new_alternatives.update({label: alternative})
        return Model(self.data, new_alternatives, self.choice)

    def remove_alternative(self, label: str) -> Model:
        """
        Remove an existing alternative.
        :param label: Name of the alternative.
        :return: Copy of the Model object without the alternative.
        :raises KeyError: No alternative with this label exists.
        """
        if label not in self.alternatives:
            raise KeyError(f'There is no alternative with the label {label}')

        new_alternatives = self.alternatives.copy()
        new_alternatives.pop(label)
        return Model(self.data, new_alternatives, self.choice)

    def set_derivative(self, label: str, derivative: FunctionalExpression) -> Model:
        """
        Add or change the function of a derivative.
        :param label: Name of the derivative.
        :param derivative: Function of the derivative.
        :return: Copy of the Model object with the new derivative.
        """
        return Model(self.data.set_derivative(label, derivative), self.alternatives, self.choice)

    def remove_derivative(self, label: str) -> Model:
        """
        Remove an existing derivative.
        :param label: Name of the derivative.
        :return: Copy of the Model object without the derivative.
        :raises KeyError: No derivative with this label exists.
        """
        return Model(self.data.remove_derivative(label), self.alternatives, self.choice)

    def set_raw_data(self, raw_data: pd.DataFrame, path: str) -> Model:
        """
        Set the input data. Further calculations are based on this data.
        :param raw_data: Input data.
        :param path: Source path of input data.
        :return: Copy of the Model object with the data.
        """
        return Model(self.data.set_raw_data(raw_data, path), self.alternatives, self.choice)

    def set_data(self, data: Data) -> Model:
        """
        Set the Data attribute. Maintains input data and derivatives.
        :param data: Data object.
        :return: Copy of the Model object with the Data object.
        """
        return Model(data, self.alternatives, self.choice)

    def get_derivative_error_report(self, label: str, variables: dict[str, object]) -> ErrorReport:
        """
        Get an error report of the derivative. Contains all found errors.
        :param label: Name of the derivative.
        :param variables: Additional variables usable in the derivative.
        :return: Error report containing all found errors.
        :raises KeyError: No derivative with this label exists.
        """
        return self.data.get_derivative_error_report(label, variables)

    def get_alternative_error_report(self, label: str, variables: dict[str, object]) -> ErrorReport:
        """
        Get an error report of the alternative. Contains all found errors.
        :param label: Name of the alternative.
        :param variables: Additional variables usable in the alternative.
        :return: Error report containing all found errors.
        :raises KeyError: No alternative with this label exists.
        """
        if label not in self.alternatives:
            raise KeyError(f'There is no alternative with this label {label}')

        alternative_expression = self.alternatives.get(label).function
        return alternative_expression.get_error_report(**(variables | self.data.get_variables()))

    def get_availability_condition_error_report(self, label: str, variables: dict[str, object]) -> ErrorReport:
        """
        Get an error report of the alternative. Contains all found errors.
        :param label: Name of the alternative.
        :param variables: Additional variables usable in the alternative.
        :return: Error report containing all found errors.
        :raises KeyError: No alternative with this label exists.
        """
        if label not in self.alternatives:
            raise KeyError(f'There is no alternative with this label {label}')

        expr = self.alternatives.get(label).availability_condition
        return expr.get_error_report(**variables)

    def set_choice(self, choice: FunctionalExpression) -> Model:
        """
        Set the choice function of the Model.
        :param choice: New choice function.
        :return: Copy of the Model with the new choice function.
        """
        return Model(self.data, self.alternatives, choice)
