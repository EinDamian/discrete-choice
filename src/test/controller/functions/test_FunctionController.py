from __future__ import annotations

from src.controller.functions.FunctionController import FunctionController

import unittest
from parameterized import parameterized


class TestFunctionController(unittest.TestCase):
    def setUp(self):
        self.fc = FunctionController()

    @parameterized.expand([
        ('abc', 'abc', True),
        ('abc123', 'abc123', True),
        ('abc123', 'abc123def456', True),
        ('whitespace', 'abc def', False),
        ('num_prefix', '123abc', False),
        ('invalid_chars1', '$abc', False),
        ('invalid_chars2', '--abc', False),
        ('invalid_chars3', 'i--abc', False),
        ('invalid_chars4', 'äabc', False),
        ('invalid_chars5', '%abc', False),
        ('invalid_chars6', '#abc', False),
        ('invalid_chars7', '#abc', False),
        ('invalid_chars8', '\'abc', False),
    ])
    def test_validate(self, name: str, label: str, allowed: bool):
        self.assertEqual(self.fc.validate(label), allowed)


if __name__ == '__main__':
    unittest.main()
