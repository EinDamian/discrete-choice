from __future__ import annotations

import re

from src.controller.AbstractController import AbstractController
from src.config import ConfigRegexPatterns


class FunctionController(AbstractController):
    """Class that is used to control the different types of functions and their management."""

    def add(self, label: str, function: str):
        """Blueprint for the addition of a function to the model.

        Args:
            label (str): Label under which the function will be saved.
            function (str): Functional Expression the user inputs.

        Raises:
            NotImplementedError: This is an abstract function and is not implemented.
        """
        raise NotImplementedError

    def remove(self, label: str):
        """Blueprint for the removal of a function from the model.

        Args:
            label (str): The label of the function to be removed.

        Raises:
            NotImplementedError: This is an abstract function and is not implemented.
        """
        raise NotImplementedError

    def change(self, label: str, function: str):
        """Blueprint for the changing of a specified function in the model.

        Args:
            label (str): The label of the function to be changed.
            function (str): The new functional expression the user input.

        Raises:
            NotImplementedError: This is an abstract function and is not implemented.
        """
        raise NotImplementedError

    def get_error_report(self, label: str):
        """Blueprint of the accessor Method of the ErrorReport for a specified function.

        Args:
            label (str): The label that specifies the function.

        Raises:
            NotImplementedError: This is an abstract function and is not implemented.
        """
        raise NotImplementedError

    def validate(self, label: str) -> bool:
        """Validates a new label to match the Python allowed pattern.

        Args:
            label (str): The label for the function.

        Returns:
            bool: True if it is valid, else false.
        """
        pattern = re.compile(ConfigRegexPatterns.PATTERN_FUNCTION_LABEL)
        return re.match(pattern, label)
