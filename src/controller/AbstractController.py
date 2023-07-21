from __future__ import annotations

from src.model.Project import Project
from src.controller.ProjectManager import ProjectManager


class AbstractController:
    """Abstract class that serves as a connection to the ProjectManager. 
    The other controllers that are not responsible for storage or project selection 
    can access the project through the inherited method getProject() from this class.
    Since the controllers do not inherit the attribute projectManager, 
    they cannot modify it or use its functions. 
    It serves as a colleague to the ProjectManager in the 'Mediator' design pattern.
    """
    def __init__(self):
        self.__project_manager: ProjectManager = ProjectManager()

    def get_project(self) -> Project:
        """Method as an interface between the controllers and the Project from the Model package.

        Returns:
            Project: The current project snapshot.
        """
        return self.__project_manager.get_project()
    
    def save(self):
        """Method used to initiate the saving process after every step that changes the model.
        """
        self.__project_manager.save()
