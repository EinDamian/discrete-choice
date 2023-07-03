from __future__ import annotations
from dataclasses import dataclass

from src.model.data.functions.StringMarker import StringMarker


@dataclass(frozen=True)
class ErrorReport:
    _valid: bool
    _marker: list[StringMarker]
