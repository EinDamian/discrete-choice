from __future__ import annotations

from src.model.processing.Threshold import Threshold
from src.controller.FileManager import FileManager
from src.controller.AbstractController import AbstractController
from src.config import ConfigThresholdWindow as ThrCfg

import pandas as pd


class EvaluationController(AbstractController):
    """Controller used to control all changes regarding the evaluation."""
    def set_thresholds(self, thresholds: dict[str, float]):
        """
        replaces all thresholds
        :param thresholds: Dictionary of new thresholds with label and threshold
        """
        self.get_project().set_thresholds(**{la: Threshold(val) for la, val in thresholds.items()})

    def get_thresholds(self) -> dict[str, float]:
        """
        accessing method for all thresholds
        :return: Dictionary of thresholds with label and threshold
        """
        evaluation = self.get_project().get_evaluation()
        defaults = {str(label): ThrCfg.DEFAULT_THRESHOLD for label in evaluation.columns} if evaluation is not None else {}
        return defaults | {la: th.value for la, th in self.get_project().get_thresholds().items() if la in defaults}


    def get_evaluation(self) -> pd.DataFrame:
        """
        accessing method for the evaluation
        :return: DataFrame including the evaluation
        """
        return self.get_project().get_evaluation()

    def evaluate(self):
        """
        Starts evaluating the model based on the selected processing configuration.
        """
        self.get_project().evaluate()

    def is_optimizable(self):
        """
        :return: Truth value, whether an evaluation exists, which is able to optimize the model.
        """
        return self.get_project().is_optimizable()

    def optimize(self):
        """
        Starts optimizing the model based on a before calculated evaluation.
        """
        try:
            self.get_project().optimize_model()
        except ValueError as v_e:
            return v_e

    def export(self, path: str) -> bool:
        """
        exports an evaluation
        :param path: where the evaluation is exported to
        :return: True if export was successful. Else False.
        """
        result = self.get_project().get_evaluation()
        FileManager.export(path, result)
        return True
