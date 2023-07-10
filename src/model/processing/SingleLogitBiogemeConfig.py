"""This module contains only one class with the same name."""

from __future__ import annotations
from dataclasses import dataclass
import itertools

from src.model.data.Model import Model
from src.model.processing.ProcessingConfig import ProcessingConfig
from src.model.processing.Evaluation import Evaluation

import pandas as pd


@dataclass(frozen=True)
class SingleLogitBiogemeConfig(ProcessingConfig):
    """
    Implements a calculation of a single discrete choice parameter estimation with logit function using biogeme.
    """

    __DISPLAY_NAME = 'Simple Maximum-Likelihood Estimation (Biogeme)'

    def process(self, model: Model) -> Evaluation:
        from biogeme.database import Database
        from biogeme.biogeme import BIOGEME
        from biogeme.models import logit
        from biogeme.expressions import Beta

        # load raw data into biogeme database
        db = Database('biogeme_model_db', model.data.raw_data)

        # TODO: USE SYSTEMATIC EVALUATION ALGORITHM FOR ALL EXPRESSIONS (DERIVATIVES, ALTERNATIVES, AV_CONDS, CHOICE)
        # TODO: INCLUDE CONFIG-PARAMETERS FOR FREE VARIABLES

        # define derivatives in biogeme database
        for label, e in model.data.derivatives.items():
            db.DefineVariable(label, e.eval(**db.variables))

        # define beta variables in biogeme database
        # unused variables in alternatives are interpreted as beta variables
        alt_variables = set(itertools.chain.from_iterable(map(lambda e: e.variables, model.alternatives.values())))
        unused_variables = alt_variables - db.variables.keys()
        betas = {label: Beta(label, 0, None, None, 0) for label in unused_variables}

        # define alternatives in biogeme database
        alternatives = [e.function.eval(**(db.variables | betas)) for label, e in model.alternatives.items()]
        availability_conditions = [e.availability_condition.eval(**(db.variables | betas))
                                   for label, e in model.alternatives.items()]
        choice = model.choice.eval(**db.variables)

        prop = logit(dict(enumerate(alternatives, 1)), dict(enumerate(availability_conditions, 1)), choice)
        bio_model = BIOGEME(db, prop)
        bio_model.generate_html, bio_model.generate_pickle = False, False  # disable generating result files
        bio_model.modelName = 'biogeme_model'  # set model name to prevent warning from biogeme
        result = bio_model.estimate()
        return Evaluation(result.getEstimatedParameters())

    @property
    def display_name(self) -> str:
        return SingleLogitBiogemeConfig.__DISPLAY_NAME

    def set_settings(self, settings: dict[str, object]) -> SingleLogitBiogemeConfig:
        return SingleLogitBiogemeConfig(settings)
