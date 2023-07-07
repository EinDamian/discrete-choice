"""This module contains only one class with the same name."""

from __future__ import annotations
from dataclasses import dataclass

from src.model.data.Model import Model
from src.model.processing.Optimizer import Optimizer

import pandas as pd


@dataclass(frozen=True)
class Evaluation:
    """
    Class represents the evaluation of a discrete choice parameter estimation.

    Attributes:
        result: The result table created by the calculation library.
        :type result: pd.DataFrame
        optimizer: optional visitor given by calculation library, if the model can be optimized through this result
        :type optimizer: Optimizer
    """

    result: pd.DataFrame
    optimizer: Optimizer = None

    def optimize(self, model: Model) -> Model:
        """
        If a model can be optimized through this Evaluation, this function optimizes the given model.
        :param model: Model that should be optimized.
        :type model: Model
        :return: New model after optimization.
        :rtype: Model
        :raises ValueError: The model cannot be optimized.
        """

        return self.optimizer.optimize(model, self)

    @property
    def is_optimizable(self) -> bool:
        """
        Shows, whether this evaluation can optimize a model.
        :return: Truth value, whether this Evaluation contains an optimizer.
        :rtype: bool
        """
        return self.optimizer is not None
