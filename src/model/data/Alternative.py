from __future__ import annotations
from dataclasses import dataclass

from src.model.data.functions.FunctionalExpression import FunctionalExpression


@dataclass(frozen=True)
class Alternative:
    """
    Represents an alternative.
    Extends a functional expression with an additional availability condition.

    Attributes:
        function: Functional expression of the alternative.
        availability_condition: Availability of the alternative.
    """
    function: FunctionalExpression
    availability_condition: FunctionalExpression
