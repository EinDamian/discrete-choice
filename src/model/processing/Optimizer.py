"""This module contains only one class with the same name."""

from __future__ import annotations

from src.model.data.Model import Model
from src.model.processing.Evaluation import Evaluation


class Optimizer:
    """
    Interface to implement different ways for optimizing a model based on an evaluation.
    """

    def optimize(self, model: Model, evaluation: Evaluation) -> Model:
        """
        Optimizes a given Model based on a given Evaluation and returns the optimized new model.
        :param model: Model which should be optimized.
        :type model: Model
        :param evaluation: Evaluation the optimization is based on.
        :type evaluation: Evaluation
        :return: Optimized new model.
        :rtype: Model
        :raises ValueError: A parameter does not fulfill a required condition.
        """
        raise NotImplementedError
