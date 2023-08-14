import os
import unittest
from unittest.mock import patch, MagicMock, mock_open
import pandas as pd
from pandas import DataFrame

from src.config import ConfigProjectManager
from src.controller.FileManager import FileManager
from src.controller.ProjectManager import ProjectManager
from src.model.Project import Project


class TestProjectManager(unittest.TestCase):

    def setUp(self):
        self.project_manager = ProjectManager()

    def test_get_project(self):
        project = self.project_manager.get_project()
        self.assertIsInstance(project, Project)

    def test_set_project_path(self):
        first_path = '/first/project/path'
        second_path = '/second/project/path'
        self.project_manager.set_project_path(first_path)
        project = self.project_manager.get_project()
        self.assertEqual(project.path, first_path)
        self.project_manager.set_project_path(second_path)
        self.assertEqual(project.path, second_path)
        self.assertNotEqual(project.path, first_path)

    def test_new(self):
        self.project_manager.new()
        self.assertIsNotNone(self.project_manager.get_project())

    def test_open_positive(self):
        with patch("os.path.isfile") as mock_isfile, \
                patch("src.controller.FileManager.FileManager.import_") as mock_import:
            mock_isfile.return_value = True
            d = {'Value': [-4.1572853759985, 15.604213622504176, 1.3418709566126628, 1.200608759487452,
                           -0.460231977877707],
                 'Rob. Std err': [0.15215404918075845, 0.035373508374609626, 0.05686965271096924, 0.03307654974635699,
                                  0.03600771249507786],
                 'Rob. t-test': [-27.322870461762474, 441.127112901941, 23.59555391400935, 36.29788380874537,
                                 -12.781483354173616],
                 'Rob. p-value': [0.0, 0.0, 0.0, 0.0, 0.0]}
            mock_import.return_value = pd.DataFrame(data=d, index=['ASC_CAR', 'ASC_SM', 'ASC_TRAIN', 'B_COST',
                                                                   'B_TIME'])
            self.project_manager.open("test_path")
            self.assertIsNotNone(self.project_manager.get_project())
            print(self.project_manager.get_project().get_evaluation())
            print(self.project_manager.get_project().get_choice())
            print(self.project_manager.get_project().get_selected_config_index())
            print(self.project_manager.get_project().get_raw_data_path())

    def test_open_negative(self):
        with patch("os.path.isfile") as mock_isfile:
            mock_isfile.side_effect = ValueError
            result = self.project_manager.open("test_path")
            self.assertIsInstance(result, ValueError)

    def test_save_positive(self):
        with patch("src.controller.FileManager.FileManager.export") as mock_export:
            self.project_manager.new()
            self.project_manager.save("test_path")
            mock_export.assert_called()

    def test_save_negative(self):
        self.project_manager.new()
        with patch("src.controller.FileManager.FileManager.export") as mock_export:
            mock_export.side_effect = OSError("Test Error")
            result = self.project_manager.save("test_path")
            self.assertIsInstance(result, OSError)

    def test_can_undo_positive(self):
        self.project_manager.set_project_path("test_path")
        result = self.project_manager.can_undo()
        self.assertTrue(result)

    def test_can_undo_negative(self):
        result = self.project_manager.can_undo()
        self.assertFalse(result)

    def test_can_redo_positive(self):
        self.project_manager.set_project_path("test_path")
        result = self.project_manager.can_redo()
        self.assertTrue(result)

    def test_can_redo_negative(self):
        result = self.project_manager.can_redo()
        self.assertFalse(result)

    def test_undo_and_redo(self):
        result = self.project_manager.undo()
        self.assertFalse(result)
        result = self.project_manager.redo()
        self.assertFalse(result)
        self.project_manager.set_project_path("test_path")
        result = self.project_manager.redo()
        self.assertFalse(result)
        result = self.project_manager.undo()
        self.assertTrue(result)
        result = self.project_manager.redo()
        self.assertTrue(result)

    def test_import_alternatives_try(self):
        with patch("os.scandir") as mock_scandir, \
                patch("os.path.isfile") as mock_isfile:
            mock_scandir.return_value = [MagicMock(path="path/to/alternative1.json")]
            mock_isfile.return_value = True
            file_manager_mock = MagicMock()
            alternative = {'label': 'alternative1', 'function': {'expression': '3*x'},
                           'availability_condition': {'expression': '1'}, 'choice_idx': 2}
            file_manager_mock.import_.return_value = alternative
            self.project_manager.FileManager = file_manager_mock
            result = self.project_manager._import_alternatives("test_path")
            self.assertEqual(result, alternative)

    def test_import_alternatives_positive(self):
        alternatives_data = {
            "alternative1.json": {
                "label": "alternative1",
                "function": {
                    "expression": "func1"
                },
                "availability_condition": {
                    "expression": "avail1"
                },
                "choice_idx": "1"
            },
            "alternative2.json": {
                "label": "alternative2",
                "function": {
                    "expression": "func2"
                },
                "availability_condition": {
                    "expression": "avail2"
                },
                "choice_idx": "2"
            }
        }
        with patch("os.scandir") as mock_scandir:
            mock_scandir.return_value = [
                MagicMock(path="path/to/alternative1.json"),
                MagicMock(path="path/to/alternative2.json")
            ]
            with patch("src.controller.FileManager.FileManager.import_") as mock_import:
                mock_import.side_effect = lambda x: alternatives_data[x]

                result = self.project_manager._import_alternatives("Alternatives")

                self.assertEqual(len(result), 2)
                self.assertIn("alternative1", result)
                self.assertIn("alternative2", result)
                self.assertEqual(result["alternative1"].function.expression, "func1")
                self.assertEqual(result["alternative1"].availability_condition.expression, "avail1")
                self.assertEqual(result["alternative1"].choice_idx, 1)
                self.assertEqual(result["alternative2"].function.expression, "func2")
                self.assertEqual(result["alternative2"].availability_condition.expression, "avail2")
                self.assertEqual(result["alternative2"].choice_idx, 2)

    """ def test_import_raw_data(self):
        raw_data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        with patch('src.controller.FileManager.FileManager.import_',
                   mock_open(read_data='A,B\n1,4\n2,5\n3,6\n')) as mock_import, \
                patch('src.controller.FileManager.pd.read_csv') as mock_read_csv:
            mock_read_csv.return_value = raw_data
            mock_import.return_value = raw_data
            self.mock_project = MagicMock()
            self.project_manager.get_project = MagicMock(return_value=self.mock_project)
            self.project_manager.import_raw_data("test_path.csv")
            self.mock_project.set_raw_data.assert_called_once_with(raw_data, "test_path.csv") """


if __name__ == '__main__':
    unittest.main()
