from __future__ import annotations

from src.model.processing.Threshold import Threshold
from src.controller.FileManager import FileManager
from src.controller.AbstractController import AbstractController

import pandas as pd

class EvaluationController(FileManager, AbstractController):
    def set_thresholds(self, thresholds: dict[str, Threshold]):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_thresholds(self) -> dict[str, Threshold]:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def get_evaluation(self) -> pd.DataFrame:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def evaluate(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def optimize(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
