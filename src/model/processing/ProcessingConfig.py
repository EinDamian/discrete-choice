"""This module contains only one class with the same name."""

from __future__ import annotations
from dataclasses import dataclass, field

from src.model.data.Model import Model
from src.model.processing.Evaluation import Evaluation

import pandas as pd


@dataclass(frozen=True)
class ProcessingConfig:
    """
    This abstract class should be base class for implementations of different calculation libraries.

    Attributes:
        settings: configuration settings for process
        :type settings: dict[str, object]
    """

    settings: dict[str, object] = field(default_factory=dict)

    def process(self, model: Model) -> Evaluation:
        """
        Executes the calculation of the implemented calculation algorithm.
        :param model: Model the calculation should be calculated on
        :type model: Model
        :return: Evaluation of the algorithm.
        :rtype: Evaluation
        :raises ValueError: Model does not fulfill the required conditions.
        """
        raise NotImplementedError

    @property
    def display_name(self) -> str:
        """
        Returns the displayed name of this configuration.
        :return: Name of this configuration, which is shown to user.
        :rtype: str
        """
        raise NotImplementedError

    def set_settings(self, settings: dict[str, object]) -> ProcessingConfig:
        """
        Setter for configuration settings for process.
        :param settings: New configuration settings.
        :type settings: dict[str, object]
        :return: Copy of configuration object with new settings.
        :rtype: ProcessingConfig
        """
        raise NotImplementedError
