import os
import shutil
import unittest
from unittest.mock import MagicMock

from src.controller.ProjectManager import ProjectManager
from src.controller.functions.AlternativeController import AlternativeController
from src.model.data.Alternative import Alternative
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from parameterized import parameterized


class TestAlternativeController(unittest.TestCase):
    __BASE_PATH = f'{os.path.dirname(__file__)}/../../resources/test_resources'

    def setUp(self):
        pm = ProjectManager()
        pm.new()
        self.ac = AlternativeController()

        os.mkdir(TestAlternativeController.__BASE_PATH)

    def tearDown(self):
        shutil.rmtree(TestAlternativeController.__BASE_PATH)

    def __prepare_alternatives(self, alternatives: dict[str, Alternative]):
        self.assertDictEqual(self.ac.get_alternatives(), {})

        for label, alternative in alternatives.items():
            self.ac.add(label, alternative.availability_condition.expression, alternative.function.expression,
                        str(alternative.choice_idx))

        self.assertDictEqual(self.ac.get_alternatives(), alternatives)

    @parameterized.expand([
        ('abc', '1+2', '3*x', '2'),
        ('abc123', '-*/', 'x', '1'),
    ])
    def test_add(self, label: str, availability: str, function: str, choice_index: str):
        old_alternatives = self.ac.get_alternatives()
        self.assertDictEqual(old_alternatives, {})

        self.ac.add(label, availability, function, choice_index)
        new_alternatives = self.ac.get_alternatives()

        self.assertDictEqual(new_alternatives, old_alternatives | {
            label: Alternative(FunctionalExpression(function), FunctionalExpression(availability), int(choice_index))})

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
        self.assertDictEqual(self.ac.get_alternatives(), {})

        with self.assertRaises(ValueError):
            self.ac.add(label, 'x', '2x', '1')

    @parameterized.expand([
        ('remove', {'a': Alternative(FunctionalExpression('x+y'), FunctionalExpression('2*z'), 3),
                    'b': Alternative(FunctionalExpression('3*a+4'), FunctionalExpression('2*c'), 2),
                    'c': Alternative(FunctionalExpression('1'), FunctionalExpression('3*a'), 5)}, 'a')
    ])
    def test_remove(self, name: str, alternatives: dict[str, Alternative], remove_label: str):
        alternatives = {label: alternative for label, alternative in alternatives.items()}
        self.__prepare_alternatives(alternatives)

        self.ac.remove(remove_label)
        new_alternatives = {k: v for k, v in alternatives.items() if k != remove_label}

        self.assertDictEqual(self.ac.get_alternatives(), new_alternatives)

    @parameterized.expand([
        ('change', {'a': Alternative(FunctionalExpression('x+y'), FunctionalExpression('2*z'), 3),
                    'b': Alternative(FunctionalExpression('3*a+4'), FunctionalExpression('2*c'), 2),
                    'c': Alternative(FunctionalExpression('1'), FunctionalExpression('3*a'), 5)}, 'a', '3*x', '4*z', 1)
    ])
    def test_change_valid(self, name: str, alternatives: dict[str, Alternative], label: str, availability: str,
                          function: str, choice_index: int):
        alternatives = {label: alternative for label, alternative in alternatives.items()}
        self.__prepare_alternatives(alternatives)

        self.ac.change(label, availability, function, choice_index)

        new_alternatives = alternatives | {label: Alternative(FunctionalExpression(availability),
                                                              FunctionalExpression(function), choice_index)}
        self.assertDictEqual(self.ac.get_alternatives(), new_alternatives)

    @parameterized.expand([
        ('single_subset', {'a': Alternative(FunctionalExpression('x+y'), FunctionalExpression('3*z'), 1),
                           'b': Alternative(FunctionalExpression('3*a+4'), FunctionalExpression('5*b'), 6),
                           'c': Alternative(FunctionalExpression('1'), FunctionalExpression('4*x'), 4)}, ['a']),
        ('multiple', {'a': Alternative(FunctionalExpression('x+y'), FunctionalExpression('3*z'), 1),
                      'b': Alternative(FunctionalExpression('3*a+4'), FunctionalExpression('5*b'), 6),
                      'c': Alternative(FunctionalExpression('1'), FunctionalExpression('4*x'), 4)}, ['a', 'b']),
    ])
    def test_export_import(self, name: str, alternatives: dict[str, Alternative], export_labels: list[str]):
        target = f'{TestAlternativeController.__BASE_PATH}/alternatives/'
        os.mkdir(target)
        alternatives = {label: alternative for label, alternative in alternatives.items()}
        self.__prepare_alternatives(alternatives)

        self.ac.export(target, export_labels)

        ProjectManager().new()

        files = os.listdir(target)
        self.assertSetEqual(set(files), {f'{label}.json' for label in alternatives.keys() if label in export_labels})

        for f in files:
            self.ac.import_(f)

        self.assertDictEqual(self.ac.get_alternatives(),
                             {la: e for la, e in alternatives.items() if la in export_labels})

    @parameterized.expand([
        ('undefined_label', {'a': Alternative(FunctionalExpression('x+y'), FunctionalExpression('3*z'), 1),
                             'b': Alternative(FunctionalExpression('3*a+4'), FunctionalExpression('5*b'), 6),
                             'c': Alternative(FunctionalExpression('1'), FunctionalExpression('4*x'), 4)}, ['x'])
    ])
    def test_export_error(self, name: str, alternatives: dict[str, Alternative], export_labels: list[str]):
        target = f'{TestAlternativeController.__BASE_PATH}/alternatives/'
        os.mkdir(target)
        alternatives = {label: alternative for label, alternative in alternatives.items()}
        self.__prepare_alternatives(alternatives)
        with self.assertRaises(KeyError):
            self.ac.export(target, export_labels)

    @parameterized.expand([
        ('None', None),
        ('special_chars', '%*-#'),
        ('root_path_permission', '/'),
        ('path_not_existing', f'{__BASE_PATH}/folder/file.json'),
        ('file_not_existing', f'{__BASE_PATH}/file.json'),
    ])
    def test_import_path_error(self, name: str, path: str):
        with self.assertRaises(OSError):
            self.ac.import_(path)

    @parameterized.expand([
        ('missing_label', '{"availability_condition": {"expression": "1"}, "function": {"expression": "1"},'
                          '"choice_index": 1}'),
        ('missing_expression1', '{"label": "a", "availability_condition": {},'
                                '"function": {"expression": "1"}, "choice_index": 1}'),
        ('missing_expression2', '{"label": "a", "availability_condition": {"expression": "1"},'
                                '"function": {}, "choice_index": 1}'),
        ('missing_all', '{}'),
        ('missing_wrong_format', '}}}'),
    ])
    def test_import_file_error(self, name: str, file_content: str):
        target_path = f'{TestAlternativeController.__BASE_PATH}/alternatives'
        target_file = f'{target_path}/error.json'

        os.mkdir(target_path)
        f = open(target_file, 'w')
        f.write(file_content)
        f.close()

        with self.assertRaises(Exception):
            self.ac.import_(target_file)

    """

    def test_export(self):
        alternative_mock = Alternative(FunctionalExpression('x'), FunctionalExpression('1'), 0)
        self.mock_project.get_alternatives.return_value = {'alt_label': alternative_mock}
        file_manager_mock = MagicMock()
        file_manager_mock.export.return_value = True
        self.ac.FileManager = file_manager_mock
        result = self.ac.export("test_path", ['alt_label'])
        self.assertTrue(result)

    def test_import_positive(self):
        self.ac.add = MagicMock()
        file_manager_mock = MagicMock()
        file_manager_mock.import_.return_value = {'label': 'alt_label', 'availability_condition': {'expression': '1'},
                                                  'function': {'expression': '3*x'}, 'choice_idx': 2}
        self.ac.FileManager = file_manager_mock
        self.ac.import_("test_path")
        self.assertEqual(self.ac.add.call_count, 1)
        self.ac.add.assert_called_once_with('alt_label', '1', '3*x', 2)

    def test_import_negative_os_error(self):
        file_manager_mock = MagicMock()
        file_manager_mock.import_.side_effect = OSError("Test Error")
        self.ac.FileManager = file_manager_mock
        with self.assertRaises(OSError):
            self.ac.import_("invalid_path")

    def test_import_negative_key_error(self):
        file_manager_mock = MagicMock()
        file_manager_mock.import_.return_value = {'invalid_key': 'value'}
        self.ac.FileManager = file_manager_mock
        with self.assertRaises(Exception):
            self.ac.import_("test_path")"""


if __name__ == '__main__':
    unittest.main()
