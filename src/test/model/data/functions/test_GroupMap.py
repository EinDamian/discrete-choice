from __future__ import annotations

from src.model.data.functions.GroupMap import GroupMap
from src.model.data.functions.Interval import Interval

import unittest
from parameterized import parameterized


class TestInterval(unittest.TestCase):
    @parameterized.expand([
        (GroupMap([[0], [1], [2]]), 1, 2),
        (GroupMap([[0], [1], [2]]), 3, None),
        (GroupMap([[0, 1, 2], [3, 4, 5], [6, 7, 8]]), 7, 3),
        (GroupMap([[0, 1, 2], [3, 4, 5], [6, 7, 8]]), -1, None),
    ])
    def test_standard(self, groupmap: GroupMap, element, index: int | None):
        self.assertEqual(groupmap(element), index)

    @parameterized.expand([
        (GroupMap([range(0, 1), range(1, 2), range(2, 3)]), 1, 2),
        (GroupMap([range(0, 10), range(5, 10)]), 5, 1),
        (GroupMap([[x for x in range(0, 1)], [x for x in range(1, 2)]]), 1, 2),
        (GroupMap([Interval(0, 1), Interval(1, 2), Interval(2, 3)]), 1.1, 2),
        (GroupMap([Interval(0, 1), Interval(1, 2), Interval(2, 3, True, False)]), 3, None),
        (GroupMap([Interval(None, 1), Interval(1, 2), Interval(2, 3)]), -1, 1)
    ])
    def test_iterators(self, groupmap: GroupMap, element, index: int | None):
        self.assertEqual(groupmap(element), index)


if __name__ == '__main__':
    unittest.main()
