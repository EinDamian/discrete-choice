import unittest
from unittest.mock import MagicMock
from src.controller.functions.AlternativeController import AlternativeController
from src.model.data.Alternative import Alternative
from src.model.data.functions.FunctionalExpression import FunctionalExpression


class TestAlternativeController(unittest.TestCase):

    def setUp(self):
        self.controller = AlternativeController()
        self.mock_project = MagicMock()
        self.controller.get_project = MagicMock(return_value=self.mock_project)

    def test_get_alternatives(self):
        alternatives_mock = {'alt1': Alternative(FunctionalExpression('x'), FunctionalExpression('1'), 0),
                             'alt2': Alternative(FunctionalExpression('2*x'), FunctionalExpression('2'), 1)}
        self.mock_project.get_alternatives.return_value = alternatives_mock
        result = self.controller.get_alternatives()
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result['alt1'], Alternative)
        self.assertIsInstance(result['alt2'], Alternative)
        self.assertEqual(result, alternatives_mock)
        self.mock_project.get_alternatives.assert_called_once()

    def test_add_positive(self):
        label = "new_alternative"
        availability = "1"
        function = "3 * x + 1"
        choice_index = 3
        self.controller.validate = MagicMock(return_value=True)
        self.controller.save = MagicMock()
        self.controller.add(label, availability, function, str(choice_index))
        alternative = Alternative(FunctionalExpression(function), FunctionalExpression(availability), choice_index)
        self.mock_project.set_alternatives.assert_called_once_with(**{label: alternative})
        self.controller.save.assert_called_once()

    def test_add_negative(self):
        label = "new_alternative"
        availability = "1"
        function = "3 * x + 1"
        choice_index = 3
        self.controller.validate = MagicMock(return_value=False)
        with self.assertRaises(ValueError):
            self.controller.add(label, availability, function, str(choice_index))
        self.mock_project.set_alternatives.assert_not_called()

    def test_remove(self):
        label = "alt_to_remove"
        self.controller.save = MagicMock()
        self.controller.remove(label)
        self.mock_project.remove_alternatives.assert_called_once_with(label)
        self.controller.save.assert_called_once()

    def test_change_positive(self):
        label = "alt_to_change"
        availability = "1"
        function = "3 * x + 1"
        choice_index = 2
        self.controller.validate = MagicMock(return_value=True)
        self.controller.save = MagicMock()
        self.controller.change(label, availability, function, choice_index)
        alternative = Alternative(FunctionalExpression(function), FunctionalExpression(availability), choice_index)
        self.mock_project.set_alternatives.assert_called_once_with(**{label: alternative})
        self.controller.save.assert_called_once()

    def test_change_negative(self):
        label = "alt_to_change"
        availability = "1"
        function = "3 * x + 1"
        choice_index = 2
        self.controller.validate = MagicMock(return_value=False)
        with self.assertRaises(Exception):
            self.controller.change(label, availability, function, choice_index)
        self.mock_project.set_alternatives.assert_not_called()

    def test_get_error_report(self):
        label = "test_alternative"
        self.controller.get_error_report(label)
        self.mock_project.get_alternative_error_report.assert_called_once_with(label)

    def test_get_availability_condition_error_report(self):
        self.controller.get_availability_condition_error_report('label')
        self.mock_project.get_availability_condition_error_report.assert_called_once_with('label')

    def test_export(self):
        alternative_mock = Alternative(FunctionalExpression('x'), FunctionalExpression('1'), 0)
        self.mock_project.get_alternatives.return_value = {'alt_label': alternative_mock}
        file_manager_mock = MagicMock()
        file_manager_mock.export.return_value = True
        self.controller.FileManager = file_manager_mock
        result = self.controller.export("test_path", ['alt_label'])
        self.assertTrue(result)

    def test_import_positive(self):
        self.controller.add = MagicMock()
        file_manager_mock = MagicMock()
        file_manager_mock.import_.return_value = {'label': 'alt_label', 'availability_condition': {'expression': '1'}, 'function': {'expression': '3*x'}, 'choice_idx': 2}
        self.controller.FileManager = file_manager_mock
        self.controller.import_("test_path")
        self.assertEqual(self.controller.add.call_count, 1)
        self.controller.add.assert_called_once_with('alt_label', '1', '3*x', 2)

    def test_import_negative_os_error(self):
        file_manager_mock = MagicMock()
        file_manager_mock.import_.side_effect = OSError("Test Error")
        self.controller.FileManager = file_manager_mock
        with self.assertRaises(OSError):
            self.controller.import_("invalid_path")

    def test_import_negative_key_error(self):
        file_manager_mock = MagicMock()
        file_manager_mock.import_.return_value = {'invalid_key': 'value'}
        self.controller.FileManager = file_manager_mock
        with self.assertRaises(Exception):
            self.controller.import_("test_path")


if __name__ == '__main__':
    unittest.main()
