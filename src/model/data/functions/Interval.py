from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Interval:
    _begin: float
    _end: float
    _include_begin: bool = True
    _include_end: bool = True

    def __contains__(self, item: float) -> bool:
        return self._begin < item < self._end\
            or (self._include_begin and self._begin == item)\
            or (self._include_end and self._end == item)
