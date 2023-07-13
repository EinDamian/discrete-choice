from __future__ import annotations
from dataclasses import dataclass

from src.model.data.functions.FunctionalExpression import FunctionalExpression


@dataclass(frozen=True)
class Alternative:
    function: FunctionalExpression
    availability_condition: FunctionalExpression
