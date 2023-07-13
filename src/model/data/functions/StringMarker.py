from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class StringMarker:
    """
    Marking inside an expression with a message. Can be used for highlighting.

    Attributes:
        message: Message of the marking.
        begin: Begin of the marking inside the expression.
        end: Excluded end of the marking inside the expression.
        color_hex: Color of the highlight.
    """
    message: str
    begin: int
    end: int
    color_hex: int
