from __future__ import annotations

from src.model.processing.Threshold import Threshold
from src.controller.FileManager import FileManager
from src.controller.AbstractController import AbstractController

import pandas as pd


class EvaluationController(FileManager, AbstractController):
    def set_thresholds(self, thresholds: dict[str, float]):
        self.get_project().set_thresholds(**{la: Threshold(val) for la, val in thresholds.values()})

    def get_thresholds(self) -> dict[str, float]:
        return {la: th.value for la, th in self.get_project().get_thresholds().items()}

    def get_evaluation(self) -> pd.DataFrame:
        return self.get_project().get_evaluation()

    def evaluate(self):
        self.get_project().evaluate()

    def optimize(self):
        self.get_project().optimize_model()

    def export(self, path: str) -> bool:
        try:
            result = self.get_project().get_evaluation()
            # Fehlt funktion export_evaluation in Project oder wie exportieren? Und als CSV?
            return True
        except OSError:
            return False
