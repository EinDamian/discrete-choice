import unittest
from unittest.mock import MagicMock
from src.model.processing.Threshold import Threshold
from src.config import ConfigThresholdWindow as ThrCfg
import pandas as pd
from src.controller.calculation.EvaluationController import EvaluationController


class TestEvaluationController(unittest.TestCase):

    def setUp(self):
        self.controller = EvaluationController()
        self.mock_project = MagicMock()
        self.controller.get_project = MagicMock(return_value=self.mock_project)

    def test_set_thresholds_positive(self):
        thresholds = {'label1': 1.5, 'label2': 0.3}
        self.controller.set_thresholds(thresholds)
        self.mock_project.set_thresholds.assert_called_once_with(**{la: Threshold(val) for la, val in thresholds.items()})

    def test_get_thresholds_with_evaluation(self):
        mock_evaluation = pd.DataFrame(columns=['label1', 'label2'])
        self.mock_project.get_evaluation = MagicMock(return_value=mock_evaluation)
        self.mock_project.get_thresholds = MagicMock(return_value={'label1': Threshold(0.7)})
        thresholds = self.controller.get_thresholds()
        expected = {'label1': 0.7, 'label2': ThrCfg.DEFAULT_THRESHOLD}
        self.assertEqual(thresholds, expected)

    def test_get_thresholds_without_evaluation(self):
        self.mock_project.get_evaluation = MagicMock(return_value=None)
        thresholds = self.controller.get_thresholds()
        self.assertEqual(thresholds, {})

    def test_get_evaluation(self):
        mock_evaluation = pd.DataFrame(columns=['label'])
        self.mock_project.get_evaluation = MagicMock(return_value=mock_evaluation)
        evaluation = self.controller.get_evaluation()
        self.assertEqual(evaluation.columns.tolist(), ['label'])
        self.mock_project.get_evaluation.assert_called_once()

    def test_evaluate(self):
        self.controller.evaluate()
        self.mock_project.evaluate.assert_called_once()

    def test_is_optimizable(self):
        self.mock_project.is_optimizable = MagicMock(return_value=True)
        result = self.controller.is_optimizable()
        self.assertTrue(result)
        self.mock_project.is_optimizable.assert_called_once()

    def test_optimize_positive(self):
        self.controller.optimize()
        self.mock_project.optimize_model.assert_called_once()

    def test_optimize_negative(self):
        self.mock_project.optimize_model = MagicMock(side_effect=ValueError("Invalid input"))
        with self.assertRaises(ValueError):
            self.controller.optimize()

    def test_export(self):
        evaluation_mock = MagicMock(spec=pd.DataFrame)
        self.mock_project.get_evaluation.return_value = evaluation_mock
        file_manager_mock = MagicMock()
        file_manager_mock.export.return_value = True
        self.controller.FileManager = file_manager_mock
        result = self.controller.export("path/to/export")
        self.assertTrue(result)

    def test_export_negative(self):
        evaluation_mock = MagicMock(spec=pd.DataFrame)
        self.mock_project.get_evaluation.return_value = evaluation_mock
        file_manager_mock = MagicMock()
        file_manager_mock.export.return_value = OSError
        self.controller.FileManager = file_manager_mock
        with self.assertRaises(OSError):
            self.controller.export("path/to/export")


if __name__ == '__main__':
    unittest.main()
