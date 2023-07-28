from __future__ import annotations

import re

from src.controller.AbstractController import AbstractController
from src.config import ConfigRegexPatterns


class FunctionController(AbstractController):
    """Class that is used to control the different types of functions and their management."""

    def validate(self, label: str) -> bool:
        """Validates a new label to match the Python allowed pattern.

        Args:
            label (str): The label for the function.

        Returns:
            bool: True if it is valid, else false.
        """
        pattern = re.compile(ConfigRegexPatterns.PATTERN_FUNCTION_LABEL)
        return bool(re.match(pattern, label))
