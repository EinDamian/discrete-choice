from __future__ import annotations
from dataclasses import dataclass

from typing import TypeVar, Generic

T = TypeVar('T')


@dataclass(frozen=True)
class GroupMap(Generic[T]):
    """
    Represents a GroupMap callable inside FunctionalExpressions.
    A GroupMap contains ordered groups of objects and returns the index of an object.
    Returns None if the object is in no group.

    Attributes:
        groups: Ordered groups of objects.
    """
    groups: list[object]

    def __call__(self, element: T) -> int | None:
        for idx, group in enumerate(self.groups):
            if element in group:
                return idx + 1

        return None
