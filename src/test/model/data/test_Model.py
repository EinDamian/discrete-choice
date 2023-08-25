from __future__ import annotations

import unittest

import pandas as pd
from parameterized import parameterized

from src.config import ConfigExpressionErrors as Config
from src.model.data.Alternative import Alternative
from src.model.data.Data import Data
from src.model.data.Model import Model
from src.model.data.functions.ErrorReport import ErrorReport
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.Interval import Interval
from src.model.data.functions.StringMarker import StringMarker


class TestInterval(unittest.TestCase):
    @parameterized.expand([
        ('alt_one', Alternative(FunctionalExpression("2"), FunctionalExpression("3"), 2)),
        ('alt_two', Alternative(FunctionalExpression("1"), FunctionalExpression("1"), 0)),
        ('alt_three', Alternative(FunctionalExpression("3"), FunctionalExpression("3"), 2))
    ])
    def test_set_alternative(self, label: str, new_alt: Alternative):
        model = Model(Data(pd.DataFrame(data={}), None, {}),
                      {'alt_one': Alternative(FunctionalExpression("1"), FunctionalExpression("1"), 0),
                       'alt_two': Alternative(FunctionalExpression("2"), FunctionalExpression("2"), 1)},
                      FunctionalExpression("0"))
        new_model = model.set_alternative(label, new_alt)
        self.assertIsNot(new_model, model)
        self.assertEqual(new_model.data, model.data)
        self.assertDictEqual(new_model.alternatives, model.alternatives | {label: new_alt})
        self.assertEqual(new_model.choice, model.choice)

    @parameterized.expand([
        ('der_one', FunctionalExpression("2")),
        ('der_two', FunctionalExpression("1")),
        ('der_three', FunctionalExpression("3"))
    ])
    def test_set_derivative(self, label: str, new_der: FunctionalExpression):
        model = Model(Data(pd.DataFrame(data={}), None,
                           {'der_one': FunctionalExpression("1"),
                            'der_two': FunctionalExpression("2")}),
                      {}, FunctionalExpression("0"))
        new_model = model.set_derivative(label, new_der)
        self.assertIsNot(new_model, model)
        self.assertDictEqual(new_model.data.derivatives, model.data.derivatives | {label: new_der})
        self.assertDictEqual(new_model.alternatives, model.alternatives)
        self.assertEqual(new_model.choice, model.choice)

    @parameterized.expand([
        ('alt_one', {'alt_two': Alternative(FunctionalExpression("2"), FunctionalExpression("2"), 1)}),
        ('alt_two', {'alt_one': Alternative(FunctionalExpression("1"), FunctionalExpression("1"), 0)})
    ])
    def test_remove_alternative(self, label: str, expected_alts: dict[str, Alternative]):
        model = Model(Data(pd.DataFrame(data={}), None, {}),
                      {'alt_one': Alternative(FunctionalExpression("1"), FunctionalExpression("1"), 0),
                       'alt_two': Alternative(FunctionalExpression("2"), FunctionalExpression("2"), 1)},
                      FunctionalExpression("0"))
        new_model = model.remove_alternative(label)
        self.assertIsNot(new_model, model)
        self.assertEqual(new_model.data, model.data)
        self.assertDictEqual(new_model.alternatives, expected_alts)
        self.assertEqual(new_model.choice, model.choice)

    @parameterized.expand([
        ('alt_two', KeyError)
        ])
    def test_remove_unknown_alternative(self, label: str, expected_exception):
        model = Model(Data(pd.DataFrame(data={}), None, {}),
                      {'alt_one': Alternative(FunctionalExpression("1"), FunctionalExpression("1"), 0)},
                      FunctionalExpression("0"))
        with self.assertRaises(expected_exception):
            model.remove_alternative(label)

    @parameterized.expand([
        ('der_one', {'der_two': FunctionalExpression("2")}),
        ('der_two', {'der_one': FunctionalExpression("1")})
    ])
    def test_remove_derivative(self, label: str, expected_ders: dict[str, FunctionalExpression]):
        model = Model(Data(pd.DataFrame(data={}), None,
                           {'der_one': FunctionalExpression("1"),
                            'der_two': FunctionalExpression("2")}),
                      {}, FunctionalExpression("0"))
        new_model = model.remove_derivative(label)
        self.assertIsNot(new_model, model)
        self.assertDictEqual(new_model.data.derivatives, expected_ders)
        self.assertDictEqual(new_model.alternatives, model.alternatives)
        self.assertEqual(new_model.choice, model.choice)

    @parameterized.expand([
        ('der_two', KeyError)
        ])
    def test_remove_unknown_derivative(self, label: str, expected_exception):
        model = Model(Data(pd.DataFrame(data={}), None,
                           {'der_one': FunctionalExpression("1")}),
                      {}, FunctionalExpression("0"))
        with self.assertRaises(expected_exception):
            model.remove_derivative(label)

    @parameterized.expand([
        (pd.DataFrame(data={'col_1': [1, 2], 'col_2': [3, 0]})),
        (pd.DataFrame(data={'col': [0, 1]}), "directory_path")
    ])
    def test_set_raw_data(self, raw_data: pd.DataFrame, path: str):
        model = Model(Data(pd.DataFrame(data={}), None, {'der': FunctionalExpression('1')}), {},
                      FunctionalExpression('0'))
        new_model = model.set_raw_data(raw_data, path)
        self.assertIsNot(new_model, model)
        self.assertIs(new_model.data.raw_data, raw_data)
        self.assertEqual(new_model.data.raw_data_path, path)
        self.assertDictEqual(new_model.data.derivatives, model.data.derivatives)

    @parameterized.expand([
        (Data(pd.DataFrame(data={}), None, {})),
        (Data(pd.DataFrame(data={'col1': [1, 2], 'col2': [0, None]}),
              "path_directory",
              {'alt': FunctionalExpression("2.5 * a")})),
        (Data(pd.DataFrame(data={}), "", {'alt': FunctionalExpression("import()x)")}))
    ])
    def test_set_data(self, data: Data):
        model = Model(Data(pd.DataFrame(data={}), None, {}),
                      {'alt_one': Alternative(FunctionalExpression("1"), FunctionalExpression("1"), 0)},
                      FunctionalExpression("0"))
        new_model = model.set_data(data)
        self.assertIsNot(new_model, model)
        self.assertEqual(new_model.data, data)
        self.assertDictEqual(new_model.alternatives, model.alternatives)
        self.assertEqual(new_model.choice, model.choice)

    @parameterized.expand([
        ('no_error', {}, {},
         {'car': Alternative(FunctionalExpression('12.5'), FunctionalExpression("0"), 0)},
         {}, 'car',
         ErrorReport(True, set())),
        ('no_error_dependency', {'col': [1, 2]}, {'a': FunctionalExpression('12.5')},
         {'car': Alternative(FunctionalExpression('(a / col) + var'), FunctionalExpression("0"), 0)},
         {'var': 3.2}, 'car',
         ErrorReport(True, set())),
        ('error_missing_dependency', {'col': [1, 2]}, {'a': FunctionalExpression('12.5')},
         {'car': Alternative(FunctionalExpression('(a / col) + var - b'), FunctionalExpression("0"), 0)},
         {'var': 3.2}, 'car',
         ErrorReport(False, {StringMarker(Config.ERROR_VARIABLE_NON_EXISTENT.format('b'), 18, 19, Config.COLOR_HEX)}))
    ])
    def test_get_alternative_error_report(self, name: str, dataframe: dict[str, list],
                                          derivatives: dict[str, FunctionalExpression],
                                          alternatives: dict[str, Alternative], variables: dict[str, object],
                                          label: str, expected_report: ErrorReport):
        model = Model(Data(pd.DataFrame(data=dataframe), None, derivatives),
                      alternatives, FunctionalExpression("0"))
        report = model.get_alternative_error_report(label, variables)
        self.assertEqual(report, expected_report)

    def test_get_alternative_type(self):
        model = Model(Data(pd.DataFrame(), None, {'a': FunctionalExpression("2"),
                                                  'b': FunctionalExpression("Interval(1, 2)")}),
                      {'example_a': Alternative(function=FunctionalExpression("a"),
                                              availability_condition=FunctionalExpression(''), choice_idx=0),
                       'example_b': Alternative(function=FunctionalExpression("b"),
                                                availability_condition=FunctionalExpression(''), choice_idx=0)
                       },
                      FunctionalExpression("0"))

        with self.assertRaises(KeyError):
            model.get_alternative_type('example_c', {})

        self.assertEqual(model.get_alternative_type('example_a', {}), int)
        self.assertEqual(model.get_alternative_type('example_b', {}), Interval)

    @parameterized.expand([
        ('no_error', {}, {},
         {'car': Alternative(FunctionalExpression('12.5'), FunctionalExpression('0'), 0)},
         {}, 'car',
         ErrorReport(True, set())),
        ('no_error_dependency', {'col': [1, 2]}, {'a': FunctionalExpression('12.5')},
         {'car': Alternative(FunctionalExpression('(a / col) + var'), FunctionalExpression('var / 2'), 0)},
         {'var': 3.2}, 'car',
         ErrorReport(True, set())),
        ('error_syntax', {}, {},
         {'car': Alternative(FunctionalExpression('1'), FunctionalExpression('.'), 0)},
         {}, 'car',
         ErrorReport(False, {StringMarker(Config.ERROR_INVALID_SYNTAX, 0, 1, Config.COLOR_HEX)})),
        ('error_missing_dependency_alternative', {'col': [1, 2]}, {'a': FunctionalExpression('12.5')},
         {'car': Alternative(FunctionalExpression('(a / col) + var'), FunctionalExpression("car"), 0)},
         {'var': 3.2}, 'car',
         ErrorReport(False, {StringMarker(Config.ERROR_VARIABLE_NON_EXISTENT.format('car'), 0, 3, Config.COLOR_HEX)}))
    ])
    def test_get_availability_condition_error_report(self, name: str, dataframe: dict[str, list],
                                                     derivatives: dict[str, FunctionalExpression],
                                                     alternatives: dict[str, Alternative], variables: dict[str, object],
                                                     label: str, expected_report: ErrorReport):
        model = Model(Data(pd.DataFrame(data=dataframe), None, derivatives),
                      alternatives, FunctionalExpression("0"))
        report = model.get_availability_condition_error_report(label, variables)
        self.assertEqual(report, expected_report)

    def test_get_availability_condition_type(self):
        model = Model(Data(pd.DataFrame(), None, {'a': FunctionalExpression("2"),
                                                  'b': FunctionalExpression("Interval(1, 2)")}),
                      {'example_a': Alternative(function=FunctionalExpression(''),
                                              availability_condition=FunctionalExpression("a"), choice_idx=0),
                       'example_b': Alternative(function=FunctionalExpression(''),
                                                availability_condition=FunctionalExpression("b"), choice_idx=0)
                       },
                      FunctionalExpression("0"))

        with self.assertRaises(KeyError):
            model.get_availability_condition_type('example_c', {})

        self.assertEqual(model.get_availability_condition_type('example_a', {}), int)
        self.assertEqual(model.get_availability_condition_type('example_b', {}), Interval)

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
    def test_get_derivative_error_report(self, name: str, dataframe: dict[str, list],
                                         derivatives: dict[str, FunctionalExpression], variables: dict[str, object],
                                         label: str, expected_report: ErrorReport):
        model = Model(Data(pd.DataFrame(data=dataframe), None, derivatives),
                      {}, FunctionalExpression("0"))
        report = model.get_derivative_error_report(label, variables)
        self.assertEqual(report, expected_report)

    def test_get_derivative_type(self):
        model = Model(Data(pd.DataFrame(), None, {'a': FunctionalExpression("2"),
                                                  'b': FunctionalExpression("Interval(1, 2)")}), {},
                      FunctionalExpression("0"))

        with self.assertRaises(KeyError):
            model.get_derivative_type('c', {})

        self.assertEqual(model.get_derivative_type('a', {}), int)
        self.assertEqual(model.get_derivative_type('b', {}), Interval)

    def test_get_error_report_unknown_label(self):
        expected_error = KeyError
        model = Model(Data(pd.DataFrame(data={}), None, {'der': FunctionalExpression('1')}),
                      {'alt': Alternative(FunctionalExpression('2'), FunctionalExpression('0'), 1)},
                      FunctionalExpression('1'))
        with self.assertRaises(expected_error):
            model.get_alternative_error_report('alt_x', {})
        with self.assertRaises(expected_error):
            model.get_availability_condition_error_report('alt_x', {})
        with self.assertRaises(expected_error):
            model.get_derivative_error_report('der_x', {})
        with self.assertRaises(expected_error):
            model.get_alternative_error_report('der', {})
        with self.assertRaises(expected_error):
            model.get_availability_condition_error_report('der', {})
        with self.assertRaises(expected_error):
            model.get_derivative_error_report('alt', {})

    @parameterized.expand([
        (FunctionalExpression("1")),
        (FunctionalExpression("choice_idx"))
    ])
    def test_set_choice(self, choice: FunctionalExpression):
        model = Model(Data(pd.DataFrame(data={}), None, {}),
                      {'alt_one': Alternative(FunctionalExpression("1"), FunctionalExpression("1"), 0)},
                      FunctionalExpression("0"))
        new_model = model.set_choice(choice)
        self.assertIsNot(new_model, model)
        self.assertEqual(new_model.data, model.data)
        self.assertDictEqual(new_model.alternatives, model.alternatives)
        self.assertEqual(new_model.choice, choice)


if __name__ == '__main__':
    unittest.main()
