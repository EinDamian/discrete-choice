import unittest
from unittest.mock import MagicMock
from src.config import ConfigProcessingWidget
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.controller.calculation.ConfigurationController import ConfigurationController


class TestConfigurationController(unittest.TestCase):

    def setUp(self):
        self.controller = ConfigurationController()
        self.mock_project = MagicMock()
        self.controller.get_project = MagicMock(return_value=self.mock_project)

    def test_select_config_positive(self):
        self.controller.select_config(1)
        self.mock_project.set_selected_config_index.assert_called_once_with(1)

    def test_select_config_negative(self):
        self.mock_project.set_selected_config_index = MagicMock(side_effect=IndexError)
        with self.assertRaises(IndexError):
            self.controller.select_config(1000)

    def test_update_settings_item(self):
        self.mock_project.get_config_settings = MagicMock(return_value=[{'name': 'value'}])
        self.mock_project.get_selected_config_index = MagicMock(return_value=0)
        self.controller.save = MagicMock()
        self.controller.update_settings_item('name', 'new_value')
        self.mock_project.set_config_settings.assert_called_once_with(0, {'name': FunctionalExpression('new_value')})
        self.controller.save.assert_called_once()
        self.mock_project.set_choice.assert_not_called()

    def test_update_settings_item_choice(self):
        self.mock_project.get_selected_config_index.return_value = 0
        settings_mock = MagicMock()
        self.mock_project.get_config_settings.return_value = settings_mock
        self.controller.save = MagicMock()
        name = ConfigProcessingWidget.CHOICE
        value = "2 * x + 3"
        self.controller.update_settings_item(name, value)
        expression = FunctionalExpression(value)
        self.mock_project.set_choice.assert_called_once_with(expression)
        settings_mock.__setitem__.assert_not_called()
        self.mock_project.set_config_settings.assert_not_called()
        self.controller.save.assert_called_once()

    def test_update_settings_item_negative_index_error(self):
        self.mock_project.get_config_settings = MagicMock(side_effect=IndexError)
        with self.assertRaises(IndexError):
            self.controller.update_settings_item('name', 'value')

    def test_update_settings_item_negative_key_error(self):
        self.mock_project.get_config_settings = MagicMock(return_value=[{'name': 'value'}], side_effect=KeyError)
        self.mock_project.get_selected_config_index = MagicMock(return_value=0)
        with self.assertRaises(KeyError):
            self.controller.update_settings_item('non_existent_name', 'value')

    def test_get_error_report_choice(self):
        label = ConfigProcessingWidget.CHOICE
        self.mock_project.get_derivative_free_variables.return_value = ['x', 'y']
        result = self.controller.get_error_report(label, FunctionalExpression('2 * x + 3'))
        self.mock_project.get_choice_error_report.assert_called_once()
        self.assertIs(result, self.mock_project.get_choice_error_report.return_value)

    def test_get_error_report_derivative(self):
        label = "test_derivative"
        expression_mock = MagicMock(spec=FunctionalExpression)
        self.mock_project.get_derivative_free_variables.return_value = [label]
        result = self.controller.get_error_report(label, expression_mock)
        expression_mock.get_error_report.assert_called_once()
        self.assertIs(result, expression_mock.get_error_report.return_value)

    def test_get_error_report_negative(self):
        mock_expression = MagicMock()
        self.mock_project.get_derivative_free_variables = MagicMock(return_value=[])
        with self.assertRaises(KeyError):
            self.controller.get_error_report('label', mock_expression)

    def test_get_config_display_names(self):
        self.mock_project.get_config_display_names = MagicMock(return_value=['name1', 'name2'])
        names = self.controller.get_config_display_names()
        self.assertListEqual(names, ['name1', 'name2'])
        self.mock_project.get_config_display_names.assert_called_once()


if __name__ == '__main__':
    unittest.main()
