from __future__ import annotations
from dataclasses import dataclass

from src.model.data.functions.StringMarker import StringMarker


@dataclass(frozen=True)
class ErrorReport:
    """
    Error report on an expression containing found errors.

    Attributes:
        valid: True if no errors. Otherwise, False.
        marker: Found errors in the expression with messages. Can be used for highlighting.
    """
    valid: bool
    marker: set[StringMarker]
