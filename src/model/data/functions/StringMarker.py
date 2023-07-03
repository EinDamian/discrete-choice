from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class StringMarker:
    _message: str
    _begin: int
    _end: int
    _color_hex: int
