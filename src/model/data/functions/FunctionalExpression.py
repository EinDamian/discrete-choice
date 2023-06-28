from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache, cached_property

from src.model.data.functions.ErrorReport import ErrorReport

@dataclass(frozen=True)
class FunctionalExpression:
    expression: str

    @lru_cache
    def eval(self, **variables):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    @lru_cache
    def get_error_report(self, **variables) -> ErrorReport:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    @cached_property
    def variables(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    @lru_cache
    def type(self, **variables) -> type:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
