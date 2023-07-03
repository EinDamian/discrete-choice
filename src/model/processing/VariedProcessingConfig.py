from __future__ import annotations
from dataclasses import dataclass

from src.model.data.Model import Model
from src.model.processing.ProcessingConfig import ProcessingConfig
from src.model.processing.SimpleProcessingConfig import SimpleProcessingConfig
from src.model.processing.Evaluation import Evaluation

import pandas as pd

@dataclass(frozen=True)
class VariedProcessingConfig(ProcessingConfig):
    components: list[SimpleProcessingConfig]

    def process(self, model: Model) -> Evaluation:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    @property
    def display_name(self) -> str:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def set_settings(self, settings: pd.DataFrame) -> ProcessingConfig:
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
