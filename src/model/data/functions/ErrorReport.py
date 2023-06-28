from __future__ import annotations
from dataclasses import dataclass

from StringMarker import StringMarker

@dataclass(frozen=True)
class ErrorReport:
    valid: bool
    marker: list[StringMarker]
