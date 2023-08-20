import os
import shutil
import unittest
from unittest.mock import patch

from parameterized import parameterized

from src.controller.ProjectManager import ProjectManager
from src.controller.functions.AlternativeController import AlternativeController
from src.controller.functions.DerivativeController import DerivativeController
from src.model.Project import Project
from src.model.data.Alternative import Alternative
from src.model.data.functions.FunctionalExpression import FunctionalExpression


class TestProjectManager(unittest.TestCase):
    __BASE_PATH = f'{os.path.dirname(__file__)}/../../resources/test_resources'

    def setUp(self):
        self.project_manager = ProjectManager()
        self.project_manager.new()
        self.ac = AlternativeController()
        self.dc = DerivativeController()

        os.makedirs(TestProjectManager.__BASE_PATH)

    def tearDown(self):
        shutil.rmtree(TestProjectManager.__BASE_PATH)

    def __prepare_project(self, alternatives: dict[str, Alternative], derivatives: dict[str, FunctionalExpression]):
        self.assertDictEqual(self.ac.get_alternatives(), {})

        for label, alternative in alternatives.items():
            self.ac.add(label, alternative.availability_condition.expression, alternative.function.expression,
                        str(alternative.choice_idx))

        self.assertDictEqual(self.ac.get_alternatives(), alternatives)

        self.assertDictEqual(self.dc.get_derivatives(), {})

        for label, expr in derivatives.items():
            self.dc.add(label, expr.expression)

        self.assertDictEqual(self.dc.get_derivatives(), derivatives)

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

    @parameterized.expand([
        ({'a': Alternative(FunctionalExpression('x+y'), FunctionalExpression('3*z'), 1),
          'b': Alternative(FunctionalExpression('3*a+4'), FunctionalExpression('5*b'), 6),
          'c': Alternative(FunctionalExpression('1'), FunctionalExpression('4*x'), 4)},
         {'a': 'x+y+z', 'b': '3*d+2', 'c': '2*a+1'}, 2, FunctionalExpression('choice'))
    ])
    def test_save_new_open(self, alternatives: dict[str, Alternative], derivatives: dict[str, str], config_idx: int,
                           choice: FunctionalExpression):
        target = f'{TestProjectManager.__BASE_PATH}/project/'
        os.mkdir(target)
        self.project_manager.get_project().set_selected_config_index(config_idx)
        self.project_manager.get_project().set_choice(choice)
        alternatives = {label: alternative for label, alternative in alternatives.items()}
        derivatives = {label: FunctionalExpression(function) for label, function in derivatives.items()}
        self.__prepare_project(alternatives, derivatives)

        self.project_manager.save(target)

        self.project_manager.new()
        p = self.project_manager.get_project()

        self.assertEqual(p.get_alternatives(), {})
        self.assertEqual(p.get_derivatives(), {})
        self.assertEqual(p.get_selected_config_index(), 0)
        self.assertEqual(p.get_choice().expression, '')

        self.project_manager.open(target)
        pa = self.project_manager.get_project()

        self.assertEqual(pa.get_alternatives(), alternatives)
        self.assertEqual(pa.get_derivatives(), derivatives)
        self.assertEqual(pa.get_selected_config_index(), config_idx)
        self.assertEqual(pa.get_choice(), choice)

    def test_open_negative(self):
        with patch("os.path.isfile") as mock_isfile:
            mock_isfile.side_effect = ValueError
            result = self.project_manager.open("test_path")
            self.assertIsInstance(result, ValueError)

    def test_save_negative(self):
        self.project_manager.new()
        with patch("src.controller.FileManager.FileManager.export") as mock_export:
            mock_export.side_effect = OSError()
            with self.assertRaises(OSError):
                self.project_manager.save("test_path")

    """def test_undo_redo(self):
        self.assertFalse(self.project_manager.can_undo())
        self.assertFalse(self.project_manager.can_redo())
        self.project_manager.set_project_path("test_path")
        self.assertTrue(self.project_manager.can_undo())
        self.assertFalse(self.project_manager.can_redo())
        self.project_manager.undo()
        self.assertFalse(self.project_manager.can_undo())
        self.assertTrue(self.project_manager.can_redo())
        self.project_manager.redo()
        self.assertTrue(self.project_manager.can_undo())
        self.assertFalse(self.project_manager.can_redo())

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

    def test_import_raw_data(self):
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
