from __future__ import annotations
from dataclasses import dataclass, field

from src.model.data.Model import Model
from src.model.processing.Evaluation import Evaluation

import pandas as pd

@dataclass(frozen=True)
class ProcessingConfig:
    settings: pd.DataFrame = field(default_factory=pd.DataFrame)

    def process(self, model: Model) -> Evaluation:
        raise NotImplementedError

    @property
    def display_name(self) -> str:
        raise NotImplementedError

    def set_settings(self, settings: pd.DataFrame) -> ProcessingConfig:
        raise NotImplementedError
