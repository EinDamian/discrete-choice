from __future__ import annotations

from Menu import Menu
from ..controller.ProjectManager import ProjectManager

class EditMenu(Menu):
    def __init__(self):
        super().__init__()

        self.__project_manager: ProjectManager = None

        raise NotImplementedError  # TODO: IMPLEMENTIEREN

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
