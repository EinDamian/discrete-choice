from __future__ import annotations
import os, shutil
import pandas as pd

from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport
from src.model.SnapshotError import SnapshotError
from src.controller.functions.DerivativeController import DerivativeController
from src.controller.ProjectManager import ProjectManager
from src.config import ConfigFiles

import unittest
from parameterized import parameterized


class TestDerivativeController(unittest.TestCase):
    __BASE_PATH = f'{os.path.dirname(__file__)}/../../resources/test_resources'

    def setUp(self):
        pm = ProjectManager()
        pm.new()
        self.dc = DerivativeController()

        os.mkdir(TestDerivativeController.__BASE_PATH)

    def tearDown(self):
        shutil.rmtree(TestDerivativeController.__BASE_PATH)


    def __prepare_derivatives(self, derivatives: dict[str, FunctionalExpression]):
        self.assertDictEqual(self.dc.get_derivatives(), {})

        for label, expr in derivatives.items():
            self.dc.add(label, expr.expression)

        self.assertDictEqual(self.dc.get_derivatives(), derivatives)

    @parameterized.expand([
        ('int', '1+1', int),
        ('float', '1+1.5', float),
        ('SyntaxError1', '++', None),
        ('SyntaxError2', 'xyz', None),
    ])
    def test_get_derivative_type(self, name: str, function: str, expected_type: type):
        label = 'label'
        self.__prepare_derivatives({label: FunctionalExpression(function)})

        t = self.dc.get_derivative_type(label)

        self.assertEqual(t, expected_type)

    @parameterized.expand([
        ('int', {'a': [1, 2, 3]}, {'a': int}),
        ('float', {'a': [1.2, 2, 3]}, {'a': float}),
    ])
    def test_get_variables(self, name: str, raw_data: pd.DataFrame, variables: dict[str, type]):
        self.assertTrue(self.dc.get_project().get_raw_data().equals(pd.DataFrame()))

        raw_data = pd.DataFrame(raw_data)
        ProjectManager().get_project().set_raw_data(raw_data, None)

        self.assertTrue(self.dc.get_project().get_raw_data().equals(raw_data))

        self.assertDictEqual(self.dc.get_variables(), variables)

    @parameterized.expand([
        ('abc', '1+2'),
        ('abc123', '-*/')
    ])
    def test_add(self, label: str, function: str):
        old_derivatives = self.dc.get_derivatives()
        self.assertDictEqual(old_derivatives, {})

        self.dc.add(label, function)
        new_derivatives = self.dc.get_derivatives()

        self.assertDictEqual(new_derivatives, old_derivatives | {label: FunctionalExpression(function)})

    @parameterized.expand([
        ('whitespace', 'abc def'),
        ('num_prefix', '123abc'),
        ('invalid_chars1', '$abc'),
        ('invalid_chars2', '--abc'),
        ('invalid_chars3', 'i--abc'),
        ('invalid_chars4', 'äabc'),
        ('invalid_chars5', '%abc'),
        ('invalid_chars6', '#abc'),
        ('invalid_chars7', '\'abc'),
    ])
    def test_add_invalid_label(self, name: str, label: str):
        self.assertDictEqual(self.dc.get_derivatives(), {})

        with self.assertRaises(ValueError):
            self.dc.add(label, '1')

    @parameterized.expand([
        ('remove', {'a': 'x+y+z', 'b': '3*a+4', 'c': '1'}, 'a')
    ])
    def test_remove_valid(self, name: str, derivatives: dict[str, str], remove_label: str):
        derivatives = {label: FunctionalExpression(function) for label, function in derivatives.items()}
        self.__prepare_derivatives(derivatives)

        self.dc.remove(remove_label)
        new_derivatives = {k: v for k, v in derivatives.items() if k != remove_label}

        self.assertDictEqual(self.dc.get_derivatives(), new_derivatives)
    @parameterized.expand([
        ('remove', {'a': 'x+y+z', 'b': '3*a+4', 'c': '1'}, 'x')
    ])
    def test_remove_invalid(self, name: str, derivatives: dict[str, str], remove_label: str):
        derivatives = {label: FunctionalExpression(function) for label, function in derivatives.items()}
        self.__prepare_derivatives(derivatives)

        with self.assertRaises(SnapshotError):
            self.dc.remove(remove_label)

    @parameterized.expand([
        ('change', {'a': 'x+y+z', 'b': '3*a+4', 'c': '1'}, 'a', '1'),
    ])
    def test_change_valid(self, name: str, derivatives: dict[str, str], label: str, function: str):
        derivatives = {label: FunctionalExpression(function) for label, function in derivatives.items()}
        self.__prepare_derivatives(derivatives)

        self.dc.change(label, function)

        new_derivative = derivatives | {label: FunctionalExpression(function)}
        self.assertDictEqual(self.dc.get_derivatives(), new_derivative)

    @parameterized.expand([
        ('single_subset', {'a': 'x+y+z', 'b': '3*a+4', 'c': '1'}, ['a']),
        ('multiple', {'a': 'x+y+z', 'b': '3*a+4', 'c': '1'}, ['a', 'b']),
    ])
    def test_export_import(self, name: str, derivatives: dict[str, str], export_labels: list[str]):
        target = f'{TestDerivativeController.__BASE_PATH}/derivatives/'
        os.mkdir(target)

        derivatives = {label: FunctionalExpression(function) for label, function in derivatives.items()}
        self.__prepare_derivatives(derivatives)

        self.dc.export(target, export_labels)

        ProjectManager().new()

        files = os.listdir(target)
        self.assertSetEqual(set(files), {f'{label}.json' for label in derivatives.keys() if label in export_labels})

        for f in files:
            self.dc.import_(f)

        self.assertDictEqual(self.dc.get_derivatives(), {la: e for la, e in derivatives.items() if la in export_labels})

    @parameterized.expand([
        ('undefined_label', {'a': 'x+y+z', 'b': '3*a+4', 'c': '1'}, ['x'])
    ])
    def test_export_keyerror(self, name: str, derivatives: dict[str, str], export_labels: list[str]):
        derivatives = {label: FunctionalExpression(function) for label, function in derivatives.items()}
        self.__prepare_derivatives(derivatives)
        with self.assertRaises(KeyError):
            self.dc.export('', export_labels)


if __name__ == '__main__':
    unittest.main()
