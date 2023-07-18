"""This module contains only one class with the same name."""

from __future__ import annotations
from dataclasses import dataclass


class SnapshotError(Exception):
    """
    Exception that will be thrown by Project in case of unable to proceed an operation on a Snapshot

    Attributes:
        parent: Exception which is responsible for this SnapshotError
    """

    def __init__(self, parent: BaseException = None):
        self.parent: BaseException = parent
