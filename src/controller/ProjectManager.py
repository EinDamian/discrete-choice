from __future__ import annotations

import json

from src.config import ConfigFiles
from src.model.Project import Project
from src.controller.FileManager import FileManager
from src.model.data.functions import FunctionalExpression
from src.model.ProjectSnapshot import ProjectSnapshot


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
        """ ps = ProjectSnapshot()
        path: str,
        previous: ProjectSnapshot = None,
        next_: ProjectSnapshot = None,
        model: Model = None,
        processing_configs:
        list[ProcessingConfig] = None,
        selected_config_index: int = 0,
        evaluation: Evaluation = None,
        thresholds: dict[str, Threshold] = None """

    def save(self, path: str = None):
        try:
            alternatives = self.get_project().get_alternatives()
            derivatives = self.get_project().get_derivatives()
            evaluation = self.get_project().get_evaluation()

            if path is not None:
                for key in alternatives:
                    self.write_alternatives(key, path)
                for key in derivatives:
                    self.write_derivatives(key, path)
                evaluation.to_csv(path + "/evaluation.csv")
                # welche weiteren Daten?
        except KeyError as k_e:
            return k_e
        except ValueError as v_e:
            return v_e

    def undo(self) -> bool:
        return self.__project.undo() is not None

    def redo(self) -> bool:
        return self.__project.redo() is not None

    def export(self, path: str) -> bool:
        """Function to export a project.

        Args:
            path (str): Path to where the project is exported.

        Returns:
            bool: True if export was successful. Else False.
        """

        try:
            alternatives = self.get_project().get_alternatives()
            derivatives = self.get_project().get_derivatives()
            evaluation = self.get_project().get_evaluation()

            for key in alternatives:
                self.export_a_d(alternatives, key, path)
            for key in derivatives:
                self.export_a_d(derivatives, key, path)

            super().export(path + "/evaluation.csv", evaluation)
            return True

        except OSError as os_e:
            return os_e

    def import_(self, path: str) -> bool:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def export_a_d(self, items: dict[str, FunctionalExpression], key: str, path: str):
        try:
            alternative = items[key]
            json_file = json.dumps(
                {
                    "label": key,
                    "functional_expression": alternative.__dict__
                }
            )
            super().export(ConfigFiles.PATH_JSON_FILE % (path, key), file_content=json_file)
        except KeyError as error:
            return error
        except OSError as os_e:
            return os_e

    def write_alternatives(self, key: str, path: str):
        try:
            f_alternative = json.dumps(self.get_project().get_alternatives()[key])
            with open(ConfigFiles.PATH_JSON_FILE % (path, key), "w") as alternative:
                alternative.write(f_alternative)
                return
        except KeyError as k_e:
            return k_e
        except ValueError as value_error:
            return value_error
        except IOError as io_error:
            return io_error

    def write_derivatives(self, key: str, path: str):
        try:
            f_derivative = json.dumps(self.get_project().get_derivatives()[key])
            with open(ConfigFiles.PATH_JSON_FILE % (path, key), "w") as derivative:
                derivative.write(f_derivative)
                return
        except KeyError as k_e:
            return k_e
        except ValueError as value_error:
            return value_error
        except IOError as io_error:
            return io_error
