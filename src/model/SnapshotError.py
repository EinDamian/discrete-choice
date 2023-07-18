"""This module contains only one class with the same name."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class SnapshotError(Exception):
    """
    Exception that will be thrown by Project in case of unable to proceed an operation on a Snapshot

    Attributes:
        parent: Exception which is responsible for this SnapshotError
    """

    parent: BaseException | None
