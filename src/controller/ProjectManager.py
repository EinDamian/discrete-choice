from __future__ import annotations

import json
import os

from src.config import ConfigFiles
from src.model.Project import Project
from src.controller.FileManager import FileManager
from src.model.ProjectSnapshot import ProjectSnapshot
from src.model.data.Alternative import Alternative
from src.model.data.Data import Data
from src.model.data.Model import Model
from src.model.data.functions import FunctionalExpression
from src.model.ProxyProject import ProxyProject
from src.model.processing import Threshold
from src.model.processing.Evaluation import Evaluation
from src.model.processing.ProcessingConfig import ProcessingConfig


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
        pm.new()
        return pm

    def get_project(self) -> Project:
        return self.__project

    def new(self):
        self.__project = ProxyProject()

    def open(self, path: str):
        try:
            evaluation = Evaluation(super().import_(path + "/evaluation.csv"))
            selected_config_index = int(super().import_(path + "/config.json"))
            alternatives = self._import_alternatives(path + "/alternatives")
            derivatives = self._import_derivatives(path + "/derivatives")
            thresholds = self._import_thresholds(path + "/thresholds")
            processing_configs = []
            for entry in os.scandir(path + "/processing_configs"):
                processing_config = ProcessingConfig(self._import_processing_config(entry.path))
                processing_configs.append(processing_config)
            data = Data(None, derivatives)  # dataframe fehlt noch
            choice = 0  # fehlt noch
            model = Model(data, alternatives, choice)

            ps = ProjectSnapshot(path, None, None, model, processing_configs, selected_config_index, evaluation, thresholds)
            self.__project = ProxyProject(ps)
        except ValueError as v_e:
            return v_e

    def save(self, path: str = None):
        try:
            evaluation = self.get_project().get_evaluation()
            config_index = self.get_project().get_selected_config_index()
            if path is not None:
                self._export(path)
                super().export(path + "/evaluation.csv", evaluation)
                super().export(path + "/config.json", str(config_index))

        except KeyError as k_e:
            return k_e
        except ValueError as v_e:
            return v_e

    def undo(self) -> bool:
        return self.__project.undo() is not None

    def redo(self) -> bool:
        return self.__project.redo() is not None

    def _export(self, path: str) -> bool:
        """Function to export all derivatives, alternatives, thresholds and processing configs.

        Args:
            path (str): Path to where the data is exported.

        Returns:
            bool: True if export was successful. Else False.
        """

        try:
            alternatives = self.get_project().get_alternatives()
            derivatives = self.get_project().get_derivatives()
            thresholds = self.get_project().get_thresholds()
            processing_configs = self.get_project().get_config_settings()
            config_names = self.get_project().get_config_display_names()
            index = 0
            for key in alternatives:
                self._export_a_d(alternatives, key, path + "/alternatives")
            for key in derivatives:
                self._export_derivative(derivatives, key, path + "/derivatives")
            for key in thresholds:
                self._export_t(thresholds, key, path + "/thresholds")
            for p_c in processing_configs:
                for key in p_c:
                    self._export_pc(p_c, key, path + "/processing_configs/" + config_names[index])
                index += 1
            return True

        except OSError as os_e:
            return os_e

    def _import_alternatives(self, path: str) -> dict[str, Alternative]:
        alternatives = {}
        for entry in os.scandir(path):
            alternative = super().import_(entry.path)
            alternatives[alternative["label"]] = Alternative(alternative["function"], alternative["availability_condition"])
        return alternatives

    def _import_derivatives(self, path: str) -> dict[str, FunctionalExpression]:
        derivatives = {}
        for entry in os.scandir(path):
            derivative = super().import_(entry.path)
            derivatives[derivative["label"]] = derivative["functional_expression"]
        return derivatives

    def _import_thresholds(self, path: str) -> dict[str, Threshold]:
        thresholds = {}
        for entry in os.scandir(path):
            threshold = super().import_(entry.path)
            thresholds[threshold["label"]] = threshold["threshold"]
        return thresholds

    def _import_processing_config(self, path: str) -> dict[str, object]:
        processing_configs = {}
        for entry in os.scandir(path):
            processing_config = super().import_(entry.path)
            processing_configs[processing_config["variable"]] = processing_config["value"]
        return processing_configs

    def _export_alternative(self, alternatives: dict[str, Alternative], key: str, path: str):
        try:
            item = alternatives[key]
            json_file = json.dumps(
                {
                    "label": key,
                    "function": item.function,
                    "availability_condition": item.availability_condition
                }
            )
            super().export(ConfigFiles.PATH_JSON_FILE % (path, key), file_content=json_file)
        except KeyError as error:
            return error
        except OSError as os_e:
            return os_e

    def _export_derivative(self, derivatives: dict[str, FunctionalExpression], key: str, path: str):
        try:
            item = derivatives[key]
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

    def _export_t(self, thresholds: dict[str, Threshold], key: str, path: str):
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

    def _export_pc(self, config_settings: dict[str, object], key: str, path: str):
        try:
            config_setting = config_settings[key]
            json_file = json.dumps(
                {
                    "variable": key,
                    "value": config_setting.__dict__
                }
            )
            super().export(ConfigFiles.PATH_JSON_FILE % (path, key), file_content=json_file)
        except KeyError as error:
            return error
        except OSError as os_e:
            return os_e
