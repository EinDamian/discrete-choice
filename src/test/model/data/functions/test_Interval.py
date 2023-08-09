from __future__ import annotations

import sys

from src.model.data.functions.Interval import Interval

import unittest
from parameterized import parameterized


class TestInterval(unittest.TestCase):
    @parameterized.expand([
        (Interval(None, None), sys.float_info.max, True),
        (Interval(None, None), sys.float_info.min, True),
        (Interval(None, 1), -1, True),
        (Interval(None, 1), 2, False),
        (Interval(-1, None), -0.5, True),
        (Interval(-1, None), -1.01, False),
        (Interval(-2, 1), -1, True),
        (Interval(-2, 1), 2, False),
        (Interval(-1, 0), -0.5, True),
        (Interval(-1, 0), -1.01, False),
    ])
    def test_standard(self, interval: Interval, item: float|None, inside: bool):
        self.assertEqual(item in interval, inside)

    @parameterized.expand([
        (Interval(0, 1, False, True), 1, True),
        (Interval(0, 1, False, True), 0, False),
        (Interval(0, 1, False, False), 0.5, True),
        (Interval(0, 1, False, False), 1, False),
    ])
    def test_ends(self, interval: Interval, item: float|None, inside: bool):
        self.assertEqual(item in interval, inside)


if __name__ == '__main__':
    unittest.main()
