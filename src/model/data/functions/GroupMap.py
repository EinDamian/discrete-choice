from __future__ import annotations
from dataclasses import dataclass

from typing import TypeVar, Generic

T = TypeVar('T')


@dataclass(frozen=True)
class GroupMap(Generic[T]):
    _groups: list[object]

    def __call__(self, element: T) -> int | None:
        for idx, group in enumerate(self._groups):
            if element in group:
                return idx + 1

        return None
