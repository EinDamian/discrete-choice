from __future__ import annotations

from ..model.Project import Project
from ProjectManager import ProjectManager

class AbstractController:
    def __init__(self):
        self.__project_manager: ProjectManager = ProjectManager()

    def get_project(self) -> Project:
        return self.__project_manager.get_project()
