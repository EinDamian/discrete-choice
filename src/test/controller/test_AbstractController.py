from __future__ import annotations
import os, shutil

from src.controller.AbstractController import AbstractController
from src.controller.ProjectManager import ProjectManager

import unittest


class TestAbstractController(unittest.TestCase):
    __BASE_PATH = f'{os.path.dirname(__file__)}/../resources/test_resources/'

    @classmethod
    def setUpClass(cls):
        os.mkdir(TestAbstractController.__BASE_PATH)

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(TestAbstractController.__BASE_PATH)

    def test_get_project(self):
        c = AbstractController()
        p = c.get_project()

        self.assertIs(p, ProjectManager().get_project())

        ProjectManager().new()

        self.assertIs(c.get_project(), ProjectManager().get_project())
        self.assertIsNot(p, ProjectManager().get_project())
        self.assertIsNot(p, c.get_project())

    def test_save(self):
        target = f'{TestAbstractController.__BASE_PATH}/project'

        c = AbstractController()
        c.get_project().set_path(target)

        c.save()

        c._AbstractController__saving_thread.join()

        self.assertTrue(os.path.isdir(target))


if __name__ == '__main__':
    unittest.main()
