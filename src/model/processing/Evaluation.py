from __future__ import annotations
from dataclasses import dataclass

from ..data.Model import Model
from Optimizer import Optimizer

import pandas as pd

@dataclass(frozen=True)
class Evaluation:
    result: pd.DataFrame
    optimizer: Optimizer | None

    def optimize(self, model: Model) -> Model:
        return self.optimizer.optimize(model, self)

    @property
    def is_optimizable(self) -> bool:
        return self.optimizer is not None
