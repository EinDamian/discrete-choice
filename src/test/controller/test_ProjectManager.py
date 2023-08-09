import unittest
from unittest.mock import patch
import pandas as pd
from src.controller.ProjectManager import ProjectManager
from src.model.Project import Project


class TestProjectManager(unittest.TestCase):

    def setUp(self):
        self.project_manager = ProjectManager()

    def test_get_project(self):
        project = self.project_manager.get_project()
        self.assertIsInstance(project, Project)

    def test_set_project_path(self):
        new_path = '/new/project/path'
        self.project_manager.set_project_path(new_path)
        project = self.project_manager.get_project()
        self.assertEqual(project.path, new_path)

    def test_new(self):
        self.project_manager.new()
        self.assertIsNotNone(self.project_manager.get_project())

    def test_open_positive(self):
        with patch("os.path.isfile") as mock_isfile, \
             patch("src.controller.FileManager.FileManager.import_") as mock_import:
            mock_isfile.return_value = True
            mock_import.return_value = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
            self.project_manager.open("test_path")
            self.assertIsNotNone(self.project_manager.get_project())

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

    def test_can_undo(self):
        result = self.project_manager.can_undo()
        self.assertFalse(result)

    def test_can_redo(self):
        result = self.project_manager.can_redo()
        self.assertFalse(result)

    def test_import_raw_data(self):
        raw_data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        with patch("src.controller.FileManager.FileManager.import_") as mock_import, \
             patch.object(self.project_manager, "_ProjectManager__project") as mock_project:
            mock_import.return_value = raw_data.to_dict()
            self.project_manager.import_raw_data("test_path")
            mock_project.set_raw_data.assert_called_once_with(raw_data, "test_path")


if __name__ == '__main__':
    unittest.main()
