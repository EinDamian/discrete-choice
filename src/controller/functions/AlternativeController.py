from __future__ import annotations

from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.controller.functions.FunctionController import FunctionController
from src.config import ConfigErrorMessages

import json

class AlternativeController(FunctionController):
    """Controller used to control all changes regarding the alternatives."""

    def get_alternatives(self) -> dict[str, FunctionalExpression]:
        """ accessing method for all the derivatives in the model.

        Returns:
            dict[str, FunctionalExpression]: dictionary with label as keys and the functional 
            expressions as values.
        """
        return self.get_project().get_alternatives()

    def add(self, label: str, function: str):
        """ validates input for safety and adds a new alternative to the model under the given 
        label.

        Args:
            label (str): the label under which the functional expression will be saved.
            function (str): user input for the functional expression.
        """
        safe_function = self.validate(function)
        if safe_function is not None:
            self.get_project().set_alternative(label, function)
        
    def remove(self, label: str):
        """ removes the alternative under the given label form the model.

        Args:
            label (str): label of the function that should be removed.
        """
        self.get_project().remove_alternative(label)

    def change(self, label: str, function: str):
        """ changes the alternative under the given label in the model.

        Args:
            label (str): the label of the alternative to be changed.
            function (str): user input for the changed function.
        """
        safe_function = self.validate(function)
        if safe_function is not None:
            self.get_project().set_alternative(label, FunctionalExpression(function))

    def get_error_report(self, label: str) -> ErrorReport:
        """Accessor Method for the errors found in the functional expression.

        Args:
            label (str): label of the alternative.

        Returns:
            ErrorReport: the error report generated for the specified alternative.
        """
        return self.get_project().get_alternative_error_report(label)

    def export(self, path: str, label: str|None = None) -> bool:
        """Function to export an alternative as a json file.

        Args:
            path (str): Path to where the File is exported.

        Returns:
            bool: True if export was successful. Else False.
        """
        try:
            alternative = self.get_project().get_alternatives[label]
            json_file = json.dumps(
                {
                    "label": label,
                    "functional_expression": alternative.__dict__
                }
            )
            super().export(path, file_content=json_file, file_type='json', filename=label)
        except KeyError as error:
            return error

    def import_(self, path: str) -> None|Exception:
        """Function to import an alternative.

        Args:
            path (str): Path to the File.

        Returns:
            bool: True if import was successful. Else False.
        """
        try:
            alternative = super().import_(path)
            self.add(alternative['label'], alternative['functional_expression']['expression'])
            return None
        except OSError:
            return Exception(ConfigErrorMessages.ERROR_MSG_IMPORT_PATH)
        