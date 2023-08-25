from __future__ import annotations

from src.model.data.Data import Data
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.ErrorReport import ErrorReport
from src.model.data.functions.StringMarker import StringMarker

from src.config import ConfigExpressionErrors as Config

import unittest
from parameterized import parameterized
import pandas as pd


class TestData(unittest.TestCase):
    @parameterized.expand([
        ('test', {'A': [0]}, 'old', {}, pd.DataFrame({'B': [1]}), 'new')
    ])
    def test_set_raw_data(self,
                          name: str,
                          raw_data: dict[str, list],
                          rd_path: str | None,
                          derivatives: dict[str, FunctionalExpression],
                          new_raw_data: pd.DataFrame,
                          new_rd_path: str | None):
        raw_data = pd.DataFrame(raw_data)
        data = Data(raw_data, rd_path, derivatives)

        self.assertEqual(data.raw_data.equals(raw_data), True)
        self.assertEqual(data.raw_data_path, rd_path)
        self.assertDictEqual(data.derivatives, derivatives)

        new_data = data.set_raw_data(new_raw_data, new_rd_path)

        self.assertIsNot(data, new_data)
        self.assertEqual(new_data.raw_data.equals(new_raw_data), True)
        self.assertEqual(new_data.raw_data_path, new_rd_path)
        self.assertDictEqual(new_data.derivatives, derivatives)

    @parameterized.expand([
        ('single_pow', {'A': [0, 1, 2, 3]}, 'old', {'der': FunctionalExpression('A**2')},
         pd.DataFrame({'A': [0, 1, 2, 3], 'der': [0, 1, 4, 9]}))
    ])
    def test_complete_data(self,
                           name: str,
                           raw_data: dict[str, list],
                           rd_path: str | None,
                           derivatives: dict[str, FunctionalExpression],
                           complete_data: pd.DataFrame):
        raw_data = pd.DataFrame(raw_data)
        data = Data(raw_data, rd_path, derivatives)

        self.assertEqual(data.raw_data.equals(raw_data), True)
        self.assertEqual(data.raw_data_path, rd_path)
        self.assertDictEqual(data.derivatives, derivatives)

        self.assertEqual(complete_data.equals(data.complete_data), True)

    @parameterized.expand([
        ('single_pow', {'A': [0, 1, 2, 3]}, 'old', 'der', FunctionalExpression('A**2'))
    ])
    def test_derivative_add_remove(self,
                                   name: str,
                                   raw_data: dict[str, list],
                                   rd_path: str | None,
                                   label: str,
                                   derivative: FunctionalExpression):
        raw_data = pd.DataFrame(raw_data)
        data = Data(raw_data, rd_path, {})

        self.assertEqual(data.raw_data.equals(raw_data), True)
        self.assertEqual(data.raw_data_path, rd_path)
        self.assertDictEqual(data.derivatives, {})

        data2 = data.set_derivative(label, derivative)

        self.assertIsNot(data, data2)
        self.assertEqual(data2.raw_data.equals(data.raw_data), True)
        self.assertEqual(data2.raw_data_path, data.raw_data_path)
        self.assertDictEqual(data2.derivatives, data.derivatives | {label: derivative})

        data3 = data2.remove_derivative(label)

        self.assertIsNot(data3, data2)
        self.assertIsNot(data3, data)
        self.assertEqual(data3, data)

    @parameterized.expand([
        ('der_two', KeyError)
    ])
    def test_remove_unknown_derivative(self, label: str, expected_exception):
        der_label = 'der_one'
        model = Data(pd.DataFrame(), None, {der_label: FunctionalExpression("1")})

        if der_label != label:
            with self.assertRaises(expected_exception):
                model.remove_derivative(label)

    @parameterized.expand([
        ('single_pow', {'A': [0, 1, 2, 3]}, 'old', {'der': FunctionalExpression('A**2')},
         {'A': FunctionalExpression('0'), 'der': FunctionalExpression('A**2')})
    ])
    def test_get_variables(self,
                           name: str,
                           raw_data: dict[str, list],
                           rd_path: str | None,
                           derivatives: dict[str, FunctionalExpression],
                           variables: dict[str, FunctionalExpression]):
        raw_data = pd.DataFrame(raw_data)
        data = Data(raw_data, rd_path, derivatives)

        self.assertDictEqual(data.get_variables(), variables)

    @parameterized.expand([
        ('no_error', {}, {'a': FunctionalExpression('12.5')},
         {}, 'a',
         ErrorReport(True, set())),
        ('no_error_dependency', {'col': [1, 2]}, {'a': FunctionalExpression('col / var')},
         {'var': 3.2}, 'a',
         ErrorReport(True, set())),
        ('error_missing_dependency', {'col': [1, 2]}, {'a': FunctionalExpression('col / var + b')},
         {'var': 3.2}, 'a',
         ErrorReport(False, {StringMarker(Config.ERROR_VARIABLE_NON_EXISTENT.format('b'), 12, 13, Config.COLOR_HEX)}))
    ])
    def test_get_derivative_error_report(self, name: str,
                                         raw_data: dict[str, list],
                                         derivatives: dict[str, FunctionalExpression],
                                         variables: dict[str, object],
                                         label: str,
                                         expected_report: ErrorReport):
        raw_data = pd.DataFrame(raw_data)
        data = Data(raw_data, None, derivatives)

        self.assertEqual(data.raw_data.equals(raw_data), True)
        self.assertDictEqual(data.derivatives, derivatives)

        report = data.get_derivative_error_report(label, variables)

        self.assertEqual(report, expected_report)

    @parameterized.expand([
        ('der_two', KeyError)
    ])
    def test_get_error_report_unknown_label(self, label: str, expected_error):
        data = Data(pd.DataFrame(), None, {'der': FunctionalExpression('1')})

        with self.assertRaises(expected_error):
            data.get_derivative_error_report(label, {})

    @parameterized.expand([
        ('add_int_float', {'a': [1], 'b': [1.5]}, {'c': FunctionalExpression('a+b')}, {}, 'c', float),
        ('add_ints', {'a': [1], 'b': [1]}, {'c': FunctionalExpression('a+b')}, {}, 'c', int)
    ])
    def test_get_derivative_type(self, name: str,
                                 raw_data: dict[str, list],
                                 derivatives: dict[str, FunctionalExpression],
                                 variables: dict[str, object],
                                 label: str,
                                 expected_type: type):
        raw_data = pd.DataFrame(raw_data)
        data = Data(raw_data, None, derivatives)

        self.assertEqual(data.raw_data.equals(raw_data), True)
        self.assertDictEqual(data.derivatives, derivatives)

        t = data.get_derivative_type(label, variables)

        self.assertEqual(t, expected_type)

    @parameterized.expand([
        ('unknown_column', {'a': [1]}, {'c': FunctionalExpression('a+b')}, {}, 'c', SyntaxError),
        ('unknown_derivative', {}, {'c': FunctionalExpression('a+b')}, {}, 'd', KeyError),
        ('self_reference', {}, {'c': FunctionalExpression('c')}, {}, 'd', KeyError),
    ])
    def test_get_derivative_type_error(self, name: str,
                                       raw_data: dict[str, list],
                                       derivatives: dict[str, FunctionalExpression],
                                       variables: dict[str, object],
                                       label: str,
                                       expected_exception):
        raw_data = pd.DataFrame(raw_data)
        data = Data(raw_data, None, derivatives)

        self.assertEqual(data.raw_data.equals(raw_data), True)
        self.assertDictEqual(data.derivatives, derivatives)

        with self.assertRaises(expected_exception):
            data.get_derivative_type(label, variables)


if __name__ == '__main__':
    unittest.main()
