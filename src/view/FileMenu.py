from __future__ import annotations

from src.view.Menu import Menu
from src.controller.ProjectManager import ProjectManager

class FileMenu(Menu):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__project_manager: ProjectManager = ProjectManager()

    def open_project(self, path: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def open_new_project(self, path: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def save_project(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def save_project_as(self, path: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def import_data(self, path: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def export_data(self, path: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
