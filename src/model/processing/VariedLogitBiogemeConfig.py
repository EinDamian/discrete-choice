"""This module contains only one class with the same name."""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Iterable

from src.model.data.Model import Model
from src.model.processing.ProcessingConfig import ProcessingConfig
from src.model.processing.SingleLogitBiogemeConfig import SingleLogitBiogemeConfig
from src.model.processing.Evaluation import Evaluation

from functools import cached_property
import pandas as pd


@dataclass(frozen=True)
class VariedLogitBiogemeConfig(ProcessingConfig):
    """
    Implements a calculation of a varied discrete choice parameter estimation with logit function using biogeme.
    The varied parameter estimation consists of multiple single parameter estimations
    (see class SimpleProcessingConfig).
    """

    __DISPLAY_NAME = 'Varied Logit Parameter Estimation (Biogeme)'

    def process(self, model: Model) -> Evaluation:
        single_result_gen = map(lambda c: c.process(model).result, self.components)  # single result generator

        # concat all single results to one DataFrame
        result = pd.concat(single_result_gen, axis=1, keys=range(len(self.components)))
        return Evaluation(result)

    @cached_property
    def components(self) -> list[SingleLogitBiogemeConfig]:
        """
        Returns the single parameter estimation configs, which are defined through this varied configuration.
        :return: List of all single parameter estimation configurations.
        :rtype: list[SingleLogitBiogemeConfig]
        """

        # Map each settings element to an iterator.
        # If the settings element is not an iterable object, an iterator with only one element will be built.
        # That is necessary to build the product over all defined option variation.
        iters = map(lambda k, v: (k, iter(v)) if isinstance(v, Iterable) else (k, iter((v,))), self.settings.items())
        product = map(dict, itertools.product(iters))  # build the product
        return list(map(SingleLogitBiogemeConfig, product))  # map all settings combinations to single configs

    @property
    def display_name(self) -> str:
        return VariedLogitBiogemeConfig.__DISPLAY_NAME

    def set_settings(self, settings: dict[str, object]) -> VariedLogitBiogemeConfig:
        return VariedLogitBiogemeConfig(settings)
