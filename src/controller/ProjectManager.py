from __future__ import annotations

import json
import os
import shutil

import pandas as pd
from pandas import DataFrame

from src.config import ConfigFiles, ConfigProjectManager
from src.model.Project import Project
from src.model.ProjectSnapshot import ProjectSnapshot
from src.model.data.Alternative import Alternative
from src.model.data.Data import Data
from src.model.data.Model import Model
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.ProxyProject import ProxyProject
from src.model.processing import Threshold
from src.model.processing.Evaluation import Evaluation
from src.controller.FileManager import FileManager


class ProjectManager:
    """class that manages changes regarding the project and is responsible for creating, saving and opening projects."""
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
        """
        Accessor method for a project.
        :return: the project.
        """
        return self.__project

    def set_project_path(self, path: str):
        """
        Sets the new project path.
        :param path: the new path for the project.
        """
        self.get_project().set_path(path)

    def new(self):
        """
        Creates a new project.
        """
        self.__project = ProxyProject()

    def open(self, path: str):
        """
        Opens a project. All relevant files are getting imported and stored from the given path. A new ProxyProject is
        created with a new ProjectSnapshot, which includes the imported data.
        :param path: path to the project that should be opened.
        """
        try:
            evaluation = None
            selected_config_index = 0
            alternatives = {}
            derivatives = {}
            thresholds = {}
            choice = FunctionalExpression("")
            raw_data_path = ""
            raw_data = pd.DataFrame()
            if os.path.isfile(os.path.join(path, ConfigProjectManager.EVALUATION)):
                eval_table: pd.DataFrame = FileManager.import_(os.path.join(path, ConfigProjectManager.EVALUATION))
                eval_table = eval_table.set_index(eval_table.columns[0])
                evaluation = Evaluation(eval_table)
            if os.path.isfile(os.path.join(path, ConfigProjectManager.CONFIG)):
                selected_config_index = int(FileManager.import_(os.path.join(path, ConfigProjectManager.CONFIG)))
            if os.path.isdir(os.path.join(path, ConfigProjectManager.ALTERNATIVES)):
                alternatives = self._import_alternatives(os.path.join(path, ConfigProjectManager.ALTERNATIVES))
            if os.path.isdir(os.path.join(path, ConfigProjectManager.DERIVATIVES)):
                derivatives = self._import_derivatives(os.path.join(path, ConfigProjectManager.DERIVATIVES))
            if os.path.isdir(os.path.join(path, ConfigProjectManager.THRESHOLDS)):
                thresholds = self._import_thresholds(os.path.join(path, ConfigProjectManager.THRESHOLDS))
            if os.path.isfile(os.path.join(path, ConfigProjectManager.CHOICE)):
                choice = FunctionalExpression(FileManager.import_(os.path.join(path, ConfigProjectManager.CHOICE))["functional_expression"]["expression"])
            if os.path.isfile(os.path.join(path, ConfigProjectManager.RAW_DATA_PATH)):
                raw_data_path = str(FileManager.import_(os.path.join(path, ConfigProjectManager.RAW_DATA_PATH))["raw_data_path"])
                if os.path.isfile(raw_data_path):
                    raw_data = FileManager.import_(raw_data_path)
            processing_configs = []
            if os.path.isdir(os.path.join(path, ConfigProjectManager.PROCESSING_CONFIGS)):
                for entry in os.scandir(os.path.join(path, ConfigProjectManager.PROCESSING_CONFIGS)):
                    if os.path.isdir(entry.path):
                        processing_config = self._import_processing_config(entry.path)
                        processing_configs.append(processing_config)
            data = Data(raw_data, raw_data_path, derivatives)
            model = Model(data, alternatives, choice)

            ps = ProjectSnapshot(path, None, None, model, None, selected_config_index, evaluation,
                                 thresholds)
            self.__project = ProxyProject(ps)
            index = 0
            for p_c in processing_configs:
                self.get_project().set_config_settings(index, p_c)
                index += 1
        except ValueError as v_e:
            return v_e

    def save(self, path: str = None):
        """
        Saves a project. Collects all the data from the project and exports them in separate files.
        :param path: path to where the project should be saved.
        """
        try:
            evaluation = self.get_project().get_evaluation()
            config_index = self.get_project().get_selected_config_index()
            if path is None:
                path = self.get_project().path
            if path is None:
                return
            self._export(path)
            if evaluation is not None:
                FileManager.export(os.path.join(path, ConfigProjectManager.EVALUATION), evaluation)
            if config_index is not None:
                FileManager.export(os.path.join(path, ConfigProjectManager.CONFIG), str(config_index))

        except KeyError as k_e:
            return k_e
        except ValueError as v_e:
            return v_e

    def can_undo(self) -> bool:
        return self.__project.can_undo()

    def undo(self) -> bool:
        """
        Reverts the last done change in the project.
        :return: True if there is a previous snapshot. Else False.
        """
        return self.__project.undo() is not None

    def can_redo(self) -> bool:
        return self.__project.can_redo()

    def redo(self) -> bool:
        """
        Reverts the last undo operation in the project.
        :return: True if there is a next snapshot. Else False.
        """
        return self.__project.redo() is not None

    def _export(self, path: str) -> bool | OSError:
        """
        Function to export choice variable, raw_data_path and all alternatives, derivatives, thresholds and
        processing configs. Clears the directory before storing, if already exists.
        :param path: Path to where the data is exported.
        :return: True if export was successful. Else False.
        :raises: OSError
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
                FileManager.export(os.path.join(path, ConfigProjectManager.CHOICE), file_content=json_choice)
            if raw_data_path is not None:
                json_raw_data_path = json.dumps(
                    {"raw_data_path": raw_data_path}
                )
                FileManager.export(os.path.join(path, ConfigProjectManager.RAW_DATA_PATH), file_content=json_raw_data_path)
            if len(alternatives) != 0:
                os.mkdir(os.path.join(path, ConfigProjectManager.ALTERNATIVES))
                for key in alternatives:
                    self._export_alternative(alternatives, key, os.path.join(path, ConfigProjectManager.ALTERNATIVES))
            if len(derivatives) != 0:
                os.mkdir(os.path.join(path, ConfigProjectManager.DERIVATIVES))
                for key in derivatives:
                    self._export_derivative(derivatives, key, os.path.join(path, ConfigProjectManager.DERIVATIVES))
            if len(thresholds) != 0:
                os.mkdir(os.path.join(path, ConfigProjectManager.THRESHOLDS))
                for key in thresholds:
                    self._export_thresholds(thresholds, key, os.path.join(path, ConfigProjectManager.THRESHOLDS))
            if processing_configs:
                os.mkdir(os.path.join(path, ConfigProjectManager.PROCESSING_CONFIGS))
                for p_c in processing_configs:
                    os.mkdir(os.path.join(path, ConfigProjectManager.PROCESSING_CONFIGS) + "/" + config_names[index])
                    for key in p_c:
                        self._export_processing_configs(p_c, key, os.path.join(path, ConfigProjectManager.PROCESSING_CONFIGS) + "/" + config_names[index])
                    index += 1
            return True

        except OSError as os_e:
            raise os_e

    def _import_alternatives(self, path: str) -> dict[str, Alternative]:
        """
        Imports all alternatives.
        :param path: path where alternatives are stored.
        :return: Dictionary with labels and Alternatives
        """
        alternatives = {}
        for entry in os.scandir(path):
            if os.path.isfile(entry.path) and entry.path.endswith(".json"):
                alternative = FileManager.import_(entry.path)
                alternatives[alternative["label"]] = Alternative(FunctionalExpression(alternative["function"]["expression"]),
                                                                 FunctionalExpression(alternative["availability_condition"]["expression"]),
                                                                 int(alternative["choice_idx"]))
        return alternatives

    def _import_derivatives(self, path: str) -> dict[str, FunctionalExpression]:
        """
        Imports all derivatives.
        :param path: path where derivatives are stored.
        :return: Dictionary with labels and FunctionalExpressions
        """
        derivatives = {}
        for entry in os.scandir(path):
            if os.path.isfile(entry.path) and entry.path.endswith(".json"):
                derivative = FileManager.import_(entry.path)
                derivatives[derivative["label"]] = FunctionalExpression(derivative["functional_expression"]["expression"])
        return derivatives

    def _import_thresholds(self, path: str) -> dict[str, Threshold]:
        """
        Imports all thresholds.
        :param path: path where thresholds are stored.
        :return: Dictionary with labels and Thresholds
        """
        thresholds = {}
        for entry in os.scandir(path):
            if os.path.isfile(entry.path) and entry.path.endswith(".json"):
                threshold = FileManager.import_(entry.path)
                thresholds[threshold["label"]] = threshold["threshold"]
        return thresholds

    def _import_processing_config(self, path: str) -> dict[str, object]:
        """
        Imports all processing_configs.
        :param path: path where processing_configs are stored.
        :return: Dictionary with labels and objects
        """
        processing_configs = {}
        for entry in os.scandir(path):
            if os.path.isfile(entry.path) and entry.path.endswith(".json"):
                processing_config = FileManager.import_(entry.path)
                processing_configs[processing_config["variable"]] = processing_config["value"]
        return processing_configs

    def _export_alternative(self, alternatives: dict[str, Alternative], key: str, path: str):
        """
        Exports an alternative as a json file.
        :param alternatives: all alternatives.
        :param key: key to get the one to be exported.
        :param path: path where the alternative should be exported to.
        """
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
        """
        Exports a derivative as a json file.
        :param derivatives: all derivatives.
        :param key: key to get the one to be exported.
        :param path: path where the derivative should be exported to.
        """
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
        """
        Exports a threshold as a json file.
        :param thresholds: all thresholds.
        :param key: key to get the one to be exported.
        :param path: path where the threshold should be exported to.
        """
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
        """
        Exports a processing_config as a json file.
        :param config_settings: all configs.
        :param key: key to get the one to be exported.
        :param path: path where the config should be exported to.
        """
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
        """
        Imports the raw_data and sets it
        :param path: path where the raw_data is located
        """
        raw_data = DataFrame(FileManager.import_(path))
        self.get_project().set_raw_data(raw_data, path)
