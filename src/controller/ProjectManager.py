from __future__ import annotations

import json

from src.config import ConfigFiles
from src.model.Project import Project
from src.controller.FileManager import FileManager
from src.model.data.functions import FunctionalExpression
from src.model.ProjectSnapshot import ProjectSnapshot
from src.model.processing import Threshold


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

    def new(self):
        raise NotImplementedError  # TODO: Implementieren

    def open(self, path: str):
        """ ps = ProjectSnapshot()
        path: str,

        model: Model = None,
        processing_configs:
        list[ProcessingConfig] = None,
        selected_config_index: int = 0,
        evaluation: Evaluation = None,
        thresholds: dict[str, Threshold] = None """

    def save(self, path: str = None):
        try:
            evaluation = self.get_project().get_evaluation()
            config_index = self.get_project().get_selected_config_index()
            # processing_configs = ?
            if path is not None:
                self.export(path)
                super().export(path + "/evaluation.csv", evaluation)
                super().export(path + "/config.json", str(config_index))
                # super().export(path + "/processing_configs.json", )

        except KeyError as k_e:
            return k_e
        except ValueError as v_e:
            return v_e

    def undo(self) -> bool:
        return self.__project.undo() is not None

    def redo(self) -> bool:
        return self.__project.redo() is not None

    def export(self, path: str) -> bool:
        """Function to export all derivatives, alternatives and thresholds.

        Args:
            path (str): Path to where the data is exported.

        Returns:
            bool: True if export was successful. Else False.
        """

        try:
            alternatives = self.get_project().get_alternatives()
            derivatives = self.get_project().get_derivatives()
            thresholds = self.get_project().get_thresholds()
            for key in alternatives:
                self.export_a_d(alternatives, key, path)
            for key in derivatives:
                self.export_a_d(derivatives, key, path)
            for key in thresholds:
                self.export_t(thresholds, key, path)
            return True

        except OSError as os_e:
            return os_e

    def import_(self, path: str) -> bool:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def export_a_d(self, items: dict[str, FunctionalExpression], key: str, path: str):
        try:
            item = items[key]
            json_file = json.dumps(
                {
                    "label": key,
                    "functional_expression": item.__dict__
                }
            )
            super().export(ConfigFiles.PATH_JSON_FILE % (path, key), file_content=json_file)
        except KeyError as error:
            return error
        except OSError as os_e:
            return os_e

    def export_t(self, thresholds: dict[str, Threshold], key: str, path: str):
        try:
            threshold = thresholds[key]
            json_file = json.dumps(
                {
                    "label": key,
                    "threshold": threshold.__dict__
                }
            )
            super().export(ConfigFiles.PATH_JSON_FILE % (path, key), file_content=json_file)
        except KeyError as error:
            return error
        except OSError as os_e:
            return os_e