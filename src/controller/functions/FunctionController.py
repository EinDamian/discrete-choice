from __future__ import annotations

from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.controller.FileManager import FileManager
from src.controller.AbstractController import AbstractController

class FunctionController(FileManager, AbstractController):
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

    def validate(self, function: str) -> FunctionalExpression:
        """Blueprint for the validation if the user input for a function. 
        When valid it returns the FunctionalExpression according to the user input.

        Args:
            function (str): The function the user input.

        Returns:
            FunctionalExpression: The functional expression as an object of how its 
            represented in the model.
        """
        return FunctionalExpression(function)

    def get_error_report(self, label: str):
        """Blueprint of the accessor Method of the ErrorReport for a specified function.

        Args:
            label (str): The label that specifies the function.

        Raises:
            NotImplementedError: This is an abstract function and is not implemented.
        """
        raise NotImplementedError
