import os
import shutil
import unittest
from unittest.mock import patch

import pandas as pd
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
        first_path = '/first_path/'
        second_path = '/second_path/'
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

    @parameterized.expand([
        ('a', Alternative(FunctionalExpression('x'), FunctionalExpression('2*y'), 2))
    ])
    def test_undo_redo(self, label: str, alternative: Alternative):
        self.assertFalse(self.project_manager.can_undo())
        self.assertFalse(self.project_manager.can_redo())
        self.ac.add(label, alternative.availability_condition.expression, alternative.function.expression,
                    str(alternative.choice_idx))
        self.assertTrue(self.project_manager.can_undo())
        self.assertFalse(self.project_manager.can_redo())
        self.project_manager.undo()
        self.assertEqual(self.project_manager.get_project().get_alternatives(), {})
        self.assertFalse(self.project_manager.can_undo())
        self.assertTrue(self.project_manager.can_redo())
        self.project_manager.redo()
        self.assertEqual(self.project_manager.get_project().get_alternatives(), {'a': alternative})
        self.assertTrue(self.project_manager.can_undo())
        self.assertFalse(self.project_manager.can_redo())

    def test_import_export_raw_data(self):
        target = f'{TestProjectManager.__BASE_PATH}/raw_data'
        os.mkdir(target)
        data_first = {
            "a": [420, 380, 790],
            "b": [50, 40, 45]
        }
        df = pd.DataFrame(data_first)
        data_second = {
            "a": [1, 2, 3],
            "b": [4, 5, 6]
        }
        dsf = pd.DataFrame(data_second)
        self.project_manager.get_project().set_raw_data(df, target)
        self.project_manager.export_raw_data(f'{target}/data.csv')
        self.project_manager.get_project().set_raw_data(dsf, target)
        self.assertFalse(self.project_manager.get_project().get_raw_data().equals(df))
        self.project_manager.import_raw_data(f'{target}/data.csv')
        self.assertTrue(self.project_manager.get_project().get_raw_data().equals(df))


if __name__ == '__main__':
    unittest.main()
