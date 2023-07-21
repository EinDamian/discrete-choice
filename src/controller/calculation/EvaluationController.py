from __future__ import annotations

from src.model.processing.Threshold import Threshold
from src.controller.FileManager import FileManager
from src.controller.AbstractController import AbstractController
from src.config import ConfigThresholdWindow as ThrCfg

import pandas as pd


class EvaluationController(AbstractController):
    def set_thresholds(self, thresholds: dict[str, float]):
        self.get_project().set_thresholds(**{la: Threshold(val) for la, val in thresholds.items()})

    def get_thresholds(self) -> dict[str, float]:
        evaluation = self.get_project().get_evaluation()
        defaults = {str(label): ThrCfg.DEFAULT_THRESHOLD for label in evaluation.columns} if evaluation is not None else {}
        return defaults | {la: th.value for la, th in self.get_project().get_thresholds().items() if la in defaults}


    def get_evaluation(self) -> pd.DataFrame:
        return self.get_project().get_evaluation()

    def evaluate(self):
        self.get_project().evaluate()

    def is_optimizable(self):
        return self.get_project().is_optimizable()

    def optimize(self):
        try:
            self.get_project().optimize_model()
        except ValueError as v_e:
            return v_e

    def export(self, path: str) -> bool:
        result = self.get_project().get_evaluation()
        FileManager.export(path, result)
        return True
