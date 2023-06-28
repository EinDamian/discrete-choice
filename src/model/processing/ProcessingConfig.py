from __future__ import annotations
from dataclasses import dataclass

from ..data.Model import Model
from Evaluation import Evaluation

import pandas as pd

@dataclass(frozen=True)
class ProcessingConfig:
    settings: pd.DataFrame

    def process(self, model: Model) -> Evaluation:
        raise NotImplementedError

    @property
    def display_name(self) -> str:
        raise NotImplementedError

    def set_settings(self, settings: pd.DataFrame) -> ProcessingConfig:
        raise NotImplementedError
