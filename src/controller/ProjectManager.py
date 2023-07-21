from __future__ import annotations

import json
import os
import shutil
from typing import Dict, Any

import pandas as pd
from pandas import DataFrame

from src.config import ConfigFiles
from src.model.Project import Project
from src.model.ProjectSnapshot import ProjectSnapshot
from src.model.data.Alternative import Alternative
from src.model.data.Data import Data
from src.model.data.Model import Model
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.ProxyProject import ProxyProject
from src.model.processing import Threshold
from src.model.processing.Evaluation import Evaluation
from src.model.processing.ProcessingConfig import ProcessingConfig
from src.controller.FileManager import FileManager


class ProjectManager:
    __instance: Project = None

    def __init__(self):
        """__init__ must be empty because it's called automatically after __new__, even if the instance already initialized."""
        pass

    def __new__(cls):
        """__new__ overload makes sure, that only one instance exists (singleton pattern)"""
        if ProjectManager.__instance is not None:
            return ProjectManager.__instance

        pm = FileManager.__new__(cls)
        pm.__project = None
        ProjectManager.__instance = pm
        pm.new()
        return pm

    def get_project(self) -> Project:
        return self.__project

    def set_project_path(self, path: str):
        self.get_project().set_path(path)

    def new(self):
        self.__project = ProxyProject()

    def open(self, path: str):
        try:
            evaluation = None
            selected_config_index = 0
            alternatives = {}
            derivatives = {}
            thresholds = {}
            choice = FunctionalExpression("")
            raw_data_path = ""
            raw_data = pd.DataFrame()
            if os.path.isfile(path + "/evaluation.csv"):
                evaluation = FileManager.import_(path + "/evaluation.csv")
            if os.path.isfile(path + "/config.json"):
                selected_config_index = int(FileManager.import_(path + "/config.json"))
            if os.path.isdir(path + "/alternatives"):
                alternatives = self._import_alternatives(path + "/alternatives")
            if os.path.isdir(path + "/derivatives"):
                derivatives = self._import_derivatives(path + "/derivatives")
            if os.path.isdir(path + "/thresholds"):
                thresholds = self._import_thresholds(path + "/thresholds")
            if os.path.isfile(path + "/Choice.json"):
                choice = FileManager.import_(path + "/Choice.json")["functional_expression"]["expression"]
            if os.path.isfile(path + "/raw_data_path.json"):
                raw_data_path = str(FileManager.import_(path + "/raw_data_path.json")["raw_data_path"])
                if os.path.isfile(raw_data_path):
                    raw_data = FileManager.import_(raw_data_path)
            processing_configs = []
            if os.path.isdir(path + "/processing_configs"):
                for entry in os.scandir(path + "/processing_configs"):
                    if os.path.isdir(entry.path):
                        processing_config = self._import_processing_config(entry.path)
                        processing_configs.append(processing_config)
            data = Data(raw_data, raw_data_path, derivatives)
            model = Model(data, alternatives, choice)

            ps = ProjectSnapshot(path, None, None, model, processing_configs, selected_config_index, evaluation,
                                 thresholds)
            self.__project = ProxyProject(ps)
        except ValueError as v_e:
            return v_e

    def save(self, path: str = None):
        try:
            evaluation = self.get_project().get_evaluation()
            config_index = self.get_project().get_selected_config_index()
            if path is None:
                path = self.get_project().path
            if path is None:
                return
            self._export(path)
            if evaluation is not None:
                FileManager.export(path + "/evaluation.csv", evaluation)
            if config_index is not None:
                FileManager.export(path + "/config.json", str(config_index))

        except KeyError as k_e:
            return k_e
        except ValueError as v_e:
            return v_e

    def undo(self) -> bool:
        return self.__project.undo() is not None

    def redo(self) -> bool:
        return self.__project.redo() is not None

    def _export(self, path: str) -> bool | OSError:
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
            choice = self.get_project().get_choice()
            raw_data_path = self.get_project().get_raw_data_path()
            index = 0
            if os.path.exists(path):
                shutil.rmtree(path)
            os.mkdir(path)

            if choice is not None:
                json_choice = json.dumps(
                    {
                        "functional_expression": {
                            "expression": choice.expression
                        }
                    }
                )
                FileManager.export(path + "/Choice.json", file_content=json_choice)
            if raw_data_path is not None:
                json_raw_data_path = json.dumps(
                    {"raw_data_path": raw_data_path}
                )
                FileManager.export(path + "/raw_data_path.json", file_content=json_raw_data_path)
            if len(alternatives) != 0:
                os.mkdir(path + "/alternatives")
                for key in alternatives:
                    self._export_alternative(alternatives, key, path + "/alternatives")
            if len(derivatives) != 0:
                os.mkdir(path + "/derivatives")
                for key in derivatives:
                    self._export_derivative(derivatives, key, path + "/derivatives")
            if len(thresholds) != 0:
                os.mkdir(path + "/thresholds")
                for key in thresholds:
                    self._export_thresholds(thresholds, key, path + "/thresholds")
            if processing_configs:
                os.mkdir(path + "/processing_configs")
                for p_c in processing_configs:
                    os.mkdir(path + "/processing_configs/" + config_names[index])
                    for key in p_c:
                        self._export_processing_configs(p_c, key, path + "/processing_configs/" + config_names[index])
                    index += 1
            return True

        except OSError as os_e:
            return os_e

    def _import_alternatives(self, path: str) -> dict[Any, Alternative] | None:
        alternatives = {}
        for entry in os.scandir(path):
            if os.path.isfile(entry.path):
                alternative = FileManager.import_(entry.path)
                alternatives[alternative["label"]] = Alternative(alternative["function"]["expression"],
                                                                 alternative["availability_condition"]["expression"],
                                                                 int(alternative["choice_idx"]))
        return alternatives

    def _import_derivatives(self, path: str) -> dict[str, FunctionalExpression] | None:
        derivatives = {}
        for entry in os.scandir(path):
            if os.path.isfile(entry.path):
                derivative = FileManager.import_(entry.path)
                derivatives[derivative["label"]] = FunctionalExpression(derivative["functional_expression"]["expression"])
        return derivatives

    def _import_thresholds(self, path: str) -> dict[str, Threshold] | None:
        thresholds = {}
        for entry in os.scandir(path):
            if os.path.isfile(entry.path):
                threshold = FileManager.import_(entry.path)
                thresholds[threshold["label"]] = threshold["threshold"]
        return thresholds

    def _import_processing_config(self, path: str) -> dict[str, object] | None:
        processing_configs = {}
        for entry in os.scandir(path):
            if os.path.isfile(entry.path):
                processing_config = FileManager.import_(entry.path)
                processing_configs[processing_config["variable"]] = processing_config["value"]
        return processing_configs

    def _export_alternative(self, alternatives: dict[str, Alternative], key: str, path: str):
        try:
            item = alternatives[key]
            json_file = json.dumps(
                {
                    "label": key,
                    "function": {
                        "expression": item.function.expression
                    },
                    "availability_condition": {
                        "expression": item.availability_condition.expression
                    },
                    "choice_idx": str(item.choice_idx)
                }
            )
            FileManager.export(ConfigFiles.PATH_JSON_FILE % (path, key), file_content=json_file)
        except KeyError as error:
            return error
        except OSError as os_e:
            return os_e

    def _export_derivative(self, derivatives: dict[str, FunctionalExpression], key: str, path: str):
        try:
            derivative = derivatives[key]
            json_file = json.dumps(
                {
                    "label": key,
                    "functional_expression": {
                        "expression": derivative.expression}
                }
            )
            FileManager.export(ConfigFiles.PATH_JSON_FILE % (path, key), file_content=json_file)
        except KeyError as error:
            return error
        except OSError as os_e:
            return os_e

    def _export_thresholds(self, thresholds: dict[str, Threshold], key: str, path: str):
        try:
            threshold = thresholds[key]
            json_file = json.dumps(
                {
                    "label": key,
                    "threshold": str(threshold.value)
                }
            )
            FileManager.export(ConfigFiles.PATH_JSON_FILE % (path, key), file_content=json_file)
        except KeyError as error:
            return error
        except OSError as os_e:
            return os_e

    def _export_processing_configs(self, config_settings: dict[str, object], key: str, path: str):
        try:
            config_setting = config_settings[key]
            json_file = json.dumps(
                {
                    "variable": key,
                    "value": str(config_setting)
                }
            )
            FileManager.export(ConfigFiles.PATH_JSON_FILE % (path, key), file_content=json_file)
        except KeyError as error:
            return error
        except OSError as os_e:
            return os_e

    def import_raw_data(self, path: str):
        raw_data = FileManager.import_(path)
        self.get_project().set_raw_data(raw_data, path)
