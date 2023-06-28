from __future__ import annotations

from src.model.Project import Project
from src.controller.ProjectManager import ProjectManager

class AbstractController:
    def __init__(self):
        self.__project_manager: ProjectManager = ProjectManager()

    def get_project(self) -> Project:
        return self.__project_manager.get_project()
