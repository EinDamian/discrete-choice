from __future__ import annotations

from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport
from src.model.data.functions.StringMarker import StringMarker
from src.config import ConfigExpressionErrors as Config

import unittest
from parameterized import parameterized
import pandas as pd


class TestFunctionalExpression(unittest.TestCase):
    @parameterized.expand([
        ('a == b', {'a', 'b'}),
        ('sum(x)', {'x'}),
        ('Interval(x)', {'x'}),
        ('GroupMap(x, y)(z)', {'x', 'y', 'z'}),
        ('f(x)', {'f', 'x'}),
        ('Interval(x)', {'x'}),
        ('(lambda x: x+1)(z)', {'z'})
    ])
    def test_variables(self, expr: str, variables: set[str]):
        self.assertSetEqual(FunctionalExpression(expr).variables, variables)

    @parameterized.expand([
        ('bool', 'a == b', {'a': FunctionalExpression('1'), 'b': FunctionalExpression('2')}, bool),
        ('int', '1 + 3 * x', {'x': FunctionalExpression('15')}, int),
        ('pd.Series', '1 + 3 * x', {'x': pd.Series(range(10))}, pd.Series),
        ('groupmap_range1', 'GroupMap([range(0, 2), range(2, 4), range(4, 6)])(x)', {'x': FunctionalExpression('5')}, int),
    ])
    def test_type(self, name: str, expr: str, variables: dict[str, object], type_: type):
        self.assertEqual(FunctionalExpression(expr).type(**variables), type_)

    @parameterized.expand([
        ('eqeqeq', 'a === b', {'a': FunctionalExpression('1'), 'b': FunctionalExpression('2')},
         ErrorReport(False, {StringMarker(Config.ERROR_INVALID_SYNTAX, 4, 5, Config.COLOR_HEX)})),

        ('unknown_var', 'a == b', {'b': FunctionalExpression('2')},
         ErrorReport(False, {StringMarker(Config.ERROR_VARIABLE_NON_EXISTENT.format('a'), 0, 1, Config.COLOR_HEX)})),

        ('unknown_vars', 'a == b', {},
         ErrorReport(False, {StringMarker(Config.ERROR_VARIABLE_NON_EXISTENT.format('a'), 0, 1, Config.COLOR_HEX),
                             StringMarker(Config.ERROR_VARIABLE_NON_EXISTENT.format('b'), 5, 6, Config.COLOR_HEX)})),

        ('brackets1', ')(', {},
         ErrorReport(False, {StringMarker(Config.ERROR_UNMATCHED_BRACKET, 0, 1, Config.COLOR_HEX),
                             StringMarker(Config.ERROR_BRACKET_NOT_CLOSED, 1, 2, Config.COLOR_HEX)})),

        ('brackets2', '((', {},
         ErrorReport(False, {StringMarker(Config.ERROR_BRACKET_NOT_CLOSED, 0, 1, Config.COLOR_HEX),
                             StringMarker(Config.ERROR_BRACKET_NOT_CLOSED, 1, 2, Config.COLOR_HEX)})),

        ('contains_set', 's in set({\'abc\', \'def\', \'ghi\'})', {'s': 'def'}, ErrorReport(True, set())),

        ('invalid_var', 'a + 1', {'a': FunctionalExpression('/')},
         ErrorReport(False, {StringMarker(Config.ERROR_INVALID_VARIABLE.format('a'), 0, 1, Config.COLOR_HEX)})),

        ('cyclic_dependency', 'a + 1', {'a': FunctionalExpression('b'), 'b': FunctionalExpression('a')},
         ErrorReport(False, {StringMarker(Config.ERROR_CYCLIC_DEPENDENCY.format("['a', 'b', 'a']"), 0, 1, Config.COLOR_HEX)}))
    ])
    def test_error_report(self, name: str, expr: str, variables: dict[str, object], report: ErrorReport):
        self.assertEqual(FunctionalExpression(expr).get_error_report(**variables), report)

    @parameterized.expand([
        ('eq_false', 'a == b', {'a': FunctionalExpression('1'), 'b': FunctionalExpression('2')}, False),
        ('eq_true', 'a == b', {'a': FunctionalExpression("'qwertz'"), 'b': FunctionalExpression("'qwertz'")}, True),
        ('add', 'a + b', {'a': FunctionalExpression("'abc'"), 'b': FunctionalExpression("'def'")}, 'abcdef'),
        ('floordiv', 'a // b', {'a': FunctionalExpression('5'), 'b': FunctionalExpression('2.3')}, 2),
        ('pow_2**2', 'a ** b', {'a': FunctionalExpression('2'), 'b': FunctionalExpression('2')}, 4),
        ('pow_2**3', 'a ** b', {'a': FunctionalExpression('2'), 'b': FunctionalExpression('3')}, 8),
        ('pow_64**(1/2)', 'a ** b', {'a': FunctionalExpression('64'), 'b': FunctionalExpression('1/2')}, 8),
        ('sum_gen', 'sum(g)', {'g': (i ** 2 for i in range(10))}, 285),
        ('contains_set', 's in set({\'abc\', \'def\', \'ghi\'})', {'s': FunctionalExpression("'def'")}, True),
        ('contains_interval1', 'x in Interval(0, None)', {'x': FunctionalExpression('-3')}, False),
        ('contains_interval2', 'x in Interval(0, 2, True, False)', {'x': FunctionalExpression('2')}, False),
        ('contains_interval3', 'x in Interval(0, 2)', {'x': FunctionalExpression('1.99')}, True),
        ('groupmap_range1', 'GroupMap([range(0, 2), range(2, 4), range(4, 6)])(x)', {'x': FunctionalExpression('5')}, 3),
        ('groupmap_range2', 'GroupMap([range(0, 2), range(2, 4), range(4, 6)])(x)', {'x': FunctionalExpression('-10')}, None),
        ('groupmap_interval1', 'GroupMap([Interval(0, 2), Interval(2, 4), Interval(4, 6)])(x)', {'x': FunctionalExpression('3.9')}, 2),
        ('groupmap_interval2', 'GroupMap([Interval(None, 2), Interval(2, 4), Interval(4, 6)])(x)', {'x': FunctionalExpression('-10')}, 1),
        ('groupmap_interval3', 'GroupMap([Interval(None, 2), Interval(2, 4), Interval(4, 6)])(x)', {'x': FunctionalExpression('2')}, 1),
        ('lambda', '(lambda x: x+1)(z)', {'z': FunctionalExpression('2')}, 3)
    ])
    def test_eval(self, name: str, expr: str, variables: dict[str, object], val: object):
        self.assertEqual(FunctionalExpression(expr).eval(**variables), val)

    @parameterized.expand([
        ('while', 'while True: pass', {}, SyntaxError),
        ('import1', 'import math', {}, SyntaxError),
        ('import2', 'from math import floor', {}, SyntaxError),
        ('import3', '__import__(\'math\').floor(2.5)', {}, SyntaxError),
        ('eval_import', 'eval("__import__(\'math\').floor(2.5)")', {}, SyntaxError)
    ])
    def test_security(self, name: str, expr: str, variables: dict[str, object], expected_exception):
        e = FunctionalExpression(expr)
        with self.assertRaises(expected_exception):
            e.eval(**variables)


if __name__ == '__main__':
    unittest.main()
