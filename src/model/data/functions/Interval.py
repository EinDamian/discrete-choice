from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Interval:
    """
    Represents an Interval callable inside FunctionalExpressions.

    Attributes:
        begin: Interval begin.
        end: Interval end.
        include_begin: Interval begin is included if True.
        include_end: Interval end is included if True.
    """
    begin: float
    end: float
    include_begin: bool = True
    include_end: bool = True

    def __contains__(self, item: float) -> bool:
        return self.__begin_contains(item) and self.__end_contains(item)

    def __begin_contains(self, item: float) -> bool:
        return self.begin is None\
            or self.begin < item\
            or (self.include_begin and self.begin == item)

    def __end_contains(self, item: float) -> bool:
        return self.end is None\
            or item < self.end\
            or (self.include_end and self.end == item)
