from __future__ import annotations

from src.model.ProxyProject import ProxyProject
from src.model.ProjectSnapshot import ProjectSnapshot
from src.model.data.functions.FunctionalExpression import FunctionalExpression

import unittest
from parameterized import parameterized
import pandas as pd


class TestProxyProject(unittest.TestCase):
    def test_undo_redo(self):
        p = ProxyProject(ProjectSnapshot())
        self.assertFalse(p.can_undo())
        self.assertFalse(p.can_redo())

        d1 = {}
        d2 = {'A': FunctionalExpression('1')}

        p.set_derivatives(**d2)

        self.assertTrue(p.can_undo())
        self.assertFalse(p.can_redo())
        self.assertDictEqual(d2, p.get_derivatives())

        p.undo()

        self.assertFalse(p.can_undo())
        self.assertTrue(p.can_redo())
        self.assertDictEqual(d1, p.get_derivatives())

        p.redo()

        self.assertTrue(p.can_undo())
        self.assertFalse(p.can_redo())
        self.assertDictEqual(d2, p.get_derivatives())


if __name__ == '__main__':
    unittest.main()
