from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Interval:
    begin: float
    end: float
    include_begin: bool = True
    include_end: bool = True

    def __contains__(self, item: float) -> bool:
        return self.begin < item < self.end\
            or (self.include_begin and self.begin == item)\
            or (self.include_end and self.end == item)
