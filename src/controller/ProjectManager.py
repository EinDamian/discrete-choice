from __future__ import annotations

from src.model.Project import Project
from src.controller.FileManager import FileManager

class ProjectManager(FileManager):
    __instance: Project = None

    def __init__(self):
        """__init__ must be empty because it's called automatically after __new__, even if the instance already initialized."""
        pass

    def __new__(cls):
        """__new__ overload makes sure, that only one instance exists (singleton pattern)"""
        if ProjectManager.__instance is not None:
            return ProjectManager.__instance

        pm = super().__new__(cls)
        pm.__project = None
        ProjectManager.__instance = pm
        return pm

    def get_project(self) -> Project:
        return self.__project

    def open(self, path: str):
        self.__project.open(path)

    def save(self, path: str):
        self.__project.save(path)

    def undo(self) -> bool:
        return self.__project.undo()

    def redo(self) -> bool:
        return self.__project.redo()

    def export(self, path: str) -> bool:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def import_(self, path: str) -> bool:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
