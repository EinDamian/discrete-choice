from __future__ import annotations

from ..data.Model import Model
from Evaluation import Evaluation

class Optimizer:
    def optimize(self, model: Model, evaluation: Evaluation) -> Model:
        raise NotImplementedError
