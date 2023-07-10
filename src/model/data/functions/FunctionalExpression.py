from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache, cached_property

from src.model.data.functions.ErrorReport import ErrorReport


@dataclass(frozen=True)
class FunctionalExpression:
    expression: str

    @cached_property
    def __compiled(self):
        return compile(self.expression, '', 'eval')

    @lru_cache
    def eval(self, **variables):
        # TODO: add Group and Interval as variables
        return eval(self.expression, variables)

    @lru_cache
    def get_error_report(self, **variables) -> ErrorReport:
        # TODO: call eval method?
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    @cached_property
    def variables(self) -> set[str]:
        return set(self.__compiled.co_names) | set(self.__compiled.co_consts)  # TODO: add other vars

    @lru_cache
    def type(self, **variables) -> type:
        return type(self.eval(**variables))
        # TODO: Exceptions?
