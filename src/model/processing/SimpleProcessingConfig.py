from __future__ import annotations
from dataclasses import dataclass

from ProcessingConfig import ProcessingConfig

from ..data.Model import Model
from Evaluation import Evaluation

import pandas as pd
from biogeme import biogeme

@dataclass(frozen=True)
class SimpleProcessingConfig(ProcessingConfig):
    def process(self, model: Model) -> Evaluation:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    @property
    def display_name(self) -> str:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_settings(self, settings: pd.DataFrame) -> ProcessingConfig:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
