from __future__ import annotations

from src.model.data.functions.FunctionalExpression import FunctionalExpression, ErrorReport
from src.controller.functions.FunctionController import FunctionController
from src.config import ConfigErrorMessages, ConfigFiles
from src.controller.FileManager import FileManager
from src.model.data.Alternative import Alternative

import json


class AlternativeController(FunctionController):
    """Controller used to control all changes regarding the alternatives."""

    def get_alternatives(self) -> dict[str, Alternative]:
        """ accessing method for all the derivatives in the model.

        Returns:
            dict[str, FunctionalExpression]: dictionary with label as keys and the functional 
            expressions as values.
        """
        return self.get_project().get_alternatives()

    def add(self, label: str, availability: str, function: str):
        """ validates input for safety and adds a new alternative to the model under the given 
        label.

        Args:
            label (str): the label under which the functional expression will be saved.
            function (str): user input for the functional expression.
        """
        safe_label = self.validate(label)
        if safe_label:
            self.get_project().set_alternative(
                label, Alternative(FunctionalExpression(function),
                                   FunctionalExpression(availability)))
        else:
            raise ValueError(
                ConfigErrorMessages.ERROR_MSG_FUNCTION_LABEL_INVALID)

    def remove(self, label: str):
        """ removes the alternative under the given label form the model.

        Args:
            label (str): label of the function that should be removed.
        """
        self.get_project().remove_alternative(label)

    def change(self, label: str, availability: str, function: str):
        """ changes the alternative under the given label in the model.

        Args:
            label (str): the label of the alternative to be changed.
            function (str): user input for the changed function.
        """
        safe_function = self.validate(label)
        if safe_function:
            self.get_project().set_alternative(
                label, Alternative(FunctionalExpression(function),
                                   FunctionalExpression(availability)))
        else:
            raise Exception(ConfigErrorMessages.ERROR_MSG_FUNCTION_LABEL_INVALID)

    def get_error_report(self, label: str) -> ErrorReport:
        """Accessor Method for the errors found in the functional expression.

        Args:
            label (str): label of the alternative.

        Returns:
            ErrorReport: the error report generated for the specified alternative.
        """
        return self.get_project().get_alternative_error_report(label)

    def get_availability_condition_error_report(self, label: str) -> ErrorReport:
        """Accessor Method for the error found in the function of the Availability Condition

        Args:
            label (str): Label of the Alternative.

        Returns:
            ErrorReport: The ErrorReport of the Availability Condition.
        """
        return self.get_project().get_availability_condition_error_report(label)

    def export(self, path: str, labels: list[str]) -> bool:
        """Function to export an alternative as a json file.

        Args:
            path (str): Path to where the File is exported.

        Returns:
            bool: True if export was successful. Else False.
        """
        alternatives = self.get_project().get_alternatives()
        for label in labels:
            try:
                alternative = alternatives[label]
                json_file = json.dumps({
                    "label": label,
                    "availability_condition":{
                        "expression": alternative.availability_condition.expression
                    },
                    "function": {
                        "expression": alternative.function.expression
                    },
                }, indent=4)
                FileManager.export(ConfigFiles.PATH_JSON_FILE %
                               (path, label), file_content=json_file)
            except KeyError as error:
                raise error  # should not happen

    def import_(self, path: str) -> None | Exception:
        """Function to import an alternative.

        Args:
            path (str): Path to the File.

        Returns:
            bool: True if import was successful. Else False.
        """
        try:
            alternative = FileManager.import_(path)
            return self.add(
                alternative['label'], alternative['availability_condition']["expression"], alternative['function']['expression'])
        except OSError as os_error:
            raise OSError(
                ConfigErrorMessages.ERROR_MSG_IMPORT_PATH) from os_error
        except KeyError as key_error:
            raise Exception(ConfigErrorMessages.ERROR_MSG_FILE_FORMAT_IMPORT_JSON +
                            ConfigErrorMessages.ERROR_MSG_MISSING_KEY % (str(key_error)))
