from __future__ import annotations

from src.view.Menu import Menu
from src.controller.ProjectManager import ProjectManager

class EditMenu(Menu):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__project_manager: ProjectManager = ProjectManager()

    def cut(self, content: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def copy(self, content: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def paste(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def delete(self, content: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def find(self, content: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def select_all(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def undo(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def redo(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
