from __future__ import annotations

from src.model.data.Model import Model
from src.model.processing.Evaluation import Evaluation


class Optimizer:
    def optimize(self, model: Model, evaluation: Evaluation) -> Model:
        raise NotImplementedError
