from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache, cached_property

from src.model.data.functions.ErrorReport import ErrorReport
from src.model.data.functions.ErrorReport import StringMarker

import ast
from graphlib import TopologicalSorter


@dataclass(frozen=True)
class FunctionalExpression:
    expression: str

    @cached_property
    def __compiled(self):
        return compile(self.expression, '', 'eval')

    @lru_cache
    def eval(self, **variables):
        # TODO: add Group and Interval as variables
        variables['Interval'] = 'range'
        return eval(self.expression, {"__builtins__": {}}, variables)

    def _get_syntax_tree(self):
        tree = ast.parse(self.expression)
        return tree

    def _check_syntax(self) -> list[StringMarker]:
        syntax_errors = list()
        try:
            compile(self.expression, '', 'eval')
        except SyntaxError as e:
            syntax_errors.append(StringMarker(e.msg, e.offset, e.end_offset, 0))
        return syntax_errors

    def _check_variables(self, **variables) -> list[StringMarker]:
        class VariableVisitor(ast.NodeVisitor):
            def __init__(self):
                self.var_nodes = list()

            def visit_Name(self, node):
                self.var_nodes.append(node)
                return node

        syntax_tree = self._get_syntax_tree()
        visitor = VariableVisitor()
        visitor.visit(syntax_tree)
        found_errors = list()
        for variable in visitor.var_nodes:
            # variable name does not exist
            if variable.id not in variables:
                marker = StringMarker("Variable name {0} does not exist.".format(variable.id), variable.col_offset,
                                      variable.end_col_offset, 0)
                found_errors.append(marker)
                continue
            # ignore imported raw data variables
            if type(variables.get(variable.id)) != FunctionalExpression:
                continue
            # search for cyclic dependencies
            try:  # catch errors b
                cyclic_dependencies = self._check_cyclic_dependencies(variable.id, **variables)
                if cyclic_dependencies:
                    marker = StringMarker("Cyclic dependency {0}.".format(cyclic_dependencies[0]), variable.col_offset,
                                          variable.end_col_offset, 0)
                    found_errors.append(marker)
                    continue
            except SyntaxError:
                marker = StringMarker("Variable {0} references invalid variable.".format(variable.id),
                                      variable.col_offset, variable.end_col_offset, 0)
                found_errors.append(marker)
                continue
            # variable is invalid
            if not variables.get(variable.id).get_error_report(**variables).valid:
                marker = StringMarker("Variable {0} is not valid.".format(variable.id), variable.col_offset,
                                      variable.end_col_offset, 0)
                found_errors.append(marker)
                continue
        return found_errors

    @staticmethod
    def _check_cyclic_dependencies(label, **variables) -> list[list[str]]:
        cycles = list()

        def depth_search(variable, path):
            dependencies = variables.get(variable).variables
            for dependency in dependencies:
                # ignore nodes without dependencies
                if dependency not in variables or type(variables.get(dependency)) != FunctionalExpression:
                    continue
                # cycle detected
                if dependency in path:
                    cycle = path.copy()
                    cycle.append(dependency)
                    cycles.append(cycle)
                    return
                # recursive step
                path.append(dependency)
                depth_search(dependency, path)
                path.pop()

        depth_search(label, [label])
        return cycles

    @lru_cache
    def get_error_report(self, **variables) -> ErrorReport:
        # TODO: add Interval/Group to variables
        found_errors = list()
        # check label (not possible)

        # check blacklisted words

        # check syntax
        found_errors.extend(self._check_syntax())

        # any of the above errors make further checking impossible
        if found_errors:
            return ErrorReport(False, found_errors)

        # check used variable names for existence, cyclic dependencies and validity
        found_errors.extend(self._check_variables(**variables))

        if found_errors:
            return ErrorReport(False, found_errors)
        else:
            return ErrorReport(True, list())

    @cached_property
    def variables(self) -> set[str]:
        # TODO: catch syntax error
        return set(self.__compiled.co_names) | set(self.__compiled.co_consts)  # TODO: add other vars?

    @lru_cache
    def type(self, **variables) -> type:
        return type(self.eval(**variables))
