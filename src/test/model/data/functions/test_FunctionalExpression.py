from __future__ import annotations

from src.model.data.functions.FunctionalExpression import FunctionalExpression

import unittest
from parameterized import parameterized


class TestFunctionalExpression(unittest.TestCase):
    @parameterized.expand([
        ('eq_false', 'a == b', {'a': 1, 'b': 2}, False),
        ('eq_true', 'a == b', {'a': 'qwertz', 'b': 'qwertz'}, True),
        ('add', 'a + b', {'a': 'abc', 'b': 'def'}, 'abcdef'),
        ('floordiv', 'a // b', {'a': 5, 'b': 2.3}, 2),
        ('pow_2**2', 'a ** b', {'a': 2, 'b': 2}, 4),
        ('pow_2**3', 'a ** b', {'a': 2, 'b': 3}, 8),
        ('pow_64**(1/2)', 'a ** b', {'a': 64, 'b': 1/2}, 8),
        ('sum_gen', 'sum(g)', {'g': (i ** 2 for i in range(10))}, 285),
        ('contains_set', '\'def\' in s', {'s': {'abc', 'def', 'ghi'}}, True),
        ('contains_interval1', 'x in Interval(0, None)', {'x': -3}, False),
        ('contains_interval2', 'x in Interval(0, 2)', {'x': 2}, False),
        ('contains_interval3', 'x in Interval(0, 2)', {'x': 1.99}, True),
        ('groupmap_range1', 'GroupMap(range(0, 2), range(2, 4), range(4, 6))(x)', {'x': 5}, 3),
        ('groupmap_range2', 'GroupMap(range(0, 2), range(2, 4), range(4, 6))(x)', {'x': -10}, None),
        ('groupmap_interval1', 'GroupMap(Interval(0, 2), Interval(2, 4), Interval(4, 6))(x)', {'x': 3.9}, 2),
        ('groupmap_interval2', 'GroupMap(Interval(None, 2), Interval(2, 4), Interval(4, 6))(x)', {'x': -10}, 1),
        ('groupmap_interval3', 'GroupMap(Interval(None, 2), Interval(2, 4), Interval(4, 6))(x)', {'x': 2}, None)
    ])
    def test_eval(self, name: str, expr: str, variables: dict[str, object], val: object):
        self.assertEqual(FunctionalExpression(expr).eval(**variables), val)

    @parameterized.expand([
        ('while', 'while True: pass', {}, SyntaxError),
        ('import1', 'import math', {}, SyntaxError),
        ('import2', 'from math import floor', {}, SyntaxError),
        ('import3', '__import__(\'math\').floor(2.5)', {}, NameError),
        ('eval_import', 'eval("__import__(\'math\').floor(2.5)")', {}, NameError)
    ])
    def test_security(self, name: str, expr: str, variables: dict[str, object], expected_exception):
        e = FunctionalExpression(expr)
        with self.assertRaises(expected_exception):
            e.eval(**variables)


if __name__ == '__main__':
    unittest.main()
