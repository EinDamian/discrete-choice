from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class StringMarker:
    message: str
    begin: int
    end: int
    color_hex: int
