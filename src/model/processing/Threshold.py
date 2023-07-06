from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Threshold:
    """
    Class represents a visualization threshold which is used to emphasize special values in the output.

    Attributes:
        value: Value of the limit. All values above this limit, will be emphasized.
        :type value: float
    """

    value: float
