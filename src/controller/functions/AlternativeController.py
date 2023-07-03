from __future__ import annotations

from ...model.data.functions.FunctionalExpression import FunctionalExpression
from FunctionController import FunctionController


class AlternativeController(FunctionController):
    """Controller used to control all changes regarding the alternatives."""

    def get_alternatives(self) -> dict[str, FunctionalExpression]:
        """ accessing method for all the derivatives in the model.

        Returns:
            dict[str, FunctionalExpression]: dictionary with label as keys and the functional expressions as values.
        """
        return self.get_project().get_alternatives()

    def add(self, label: str, function: str):
        """ validates input for safety and adds a new alternative to the model under the given label.

        Args:
            label (str): the label under which the functional expression will be saved.
            function (str): user input for the functional expression.
        """
        # TODO: hier habe ich ein label eingefügt. Oder muss dass hier werzeugt werden? --> haben wir im Klassendiagramm tatsächlich vergessen
        # TODO: hier muss string rein, der Nutzer gibt ja einen string ein,
        safe_function = self.validate(function)
        if safe_function != None:
            self.get_project().set_alternative(label, function)
        else:
            return False  # TODO: falls der nutzer böse ist was passiert dann? Der muss ja iwie invalid input angezwigt bekommen?

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
        # TODO: hier muss string rein für die function, der Nutzer gibt ja einen string ein,
        safe_function = self.validate(function)
        if safe_function != None:
            self.get_project().set_alternative(label, function)

    def validate(self, function: str) -> FunctionalExpression:
        """ Dafety validation of the user input.

        Args:
            function (str): unser input for the new alternative function.

        Returns:
            FunctionalExpression: functional expression thats generated from the input. None, if input is invalid.
        """
        return super().validate(function)

    def get_error_report(self, label: str):
        """Accessor Method for the errors found in the functional expression.

        Args:
            label (str): label of the alternative.

        Returns:
            ErrorReport: the error report generated for the specified alternative.
        """
        return self.get_project().get_alternative_error_report(label)
