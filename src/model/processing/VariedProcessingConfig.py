from __future__ import annotations
from dataclasses import dataclass

from src.model.data.Model import Model
from src.model.processing.ProcessingConfig import ProcessingConfig
from src.model.processing.SimpleProcessingConfig import SimpleProcessingConfig
from src.model.processing.Evaluation import Evaluation

import pandas as pd

@dataclass(frozen=True)
class VariedProcessingConfig(ProcessingConfig):
    __DISPLAY_NAME = 'Varied Maximum-Likelihood Estimation (Biogeme)'

    components: list[SimpleProcessingConfig]

    def process(self, model: Model) -> Evaluation:
        single_result_gen = map(lambda c: c.process(model).result, self.components)  # single result generator
        result = pd.concat(single_result_gen, axis=1, keys=range(len(self.components)))  # concat all single results together to one DataFrame
        return Evaluation(result)

    @property
    def display_name(self) -> str:
        return VariedProcessingConfig.__DISPLAY_NAME

    def set_settings(self, settings: pd.DataFrame) -> VariedProcessingConfig:
        return VariedProcessingConfig(settings, self.components)

    def set_components(self, components: list[SimpleProcessingConfig]) -> VariedProcessingConfig:
        return VariedProcessingConfig(self.settings, components)
