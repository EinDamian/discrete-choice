"""This module contains only one class with the same name."""

from __future__ import annotations
from dataclasses import dataclass
from graphlib import TopologicalSorter
import functools

from src.model.data.Model import Model
from src.model.processing.ProcessingConfig import ProcessingConfig
from src.model.processing.Evaluation import Evaluation


@dataclass(frozen=True)
class SingleLogitBiogemeConfig(ProcessingConfig):
    """
    Implements a calculation of a single discrete choice parameter estimation with logit function using biogeme.
    """

    __DISPLAY_NAME = 'Logit Parameter Estimation (Biogeme)'

    def process(self, model: Model) -> Evaluation:
        from biogeme.database import Database
        from biogeme.biogeme import BIOGEME
        from biogeme.models import logit
        from biogeme.expressions import Beta

        # load raw data into biogeme database
        db = Database('biogeme_model_db', model.data.raw_data)

        derivative_depends = {label: expr.variables for label, expr in model.data.derivatives.items()}
        alternative_depends = {label: alt.function.variables for label, alt in model.alternatives.items()}
        def_depends = derivative_depends | alternative_depends

        # define derivatives in biogeme database in topological order to consider dependencies
        for label in TopologicalSorter(derivative_depends).static_order():
            expr = model.data.derivatives[label]
            db.DefineVariable(label, expr.eval(**db.variables))

        # define beta variables in biogeme database
        # undefined labels in alternatives are interpreted as beta variables
        beta_labels = functools.reduce(lambda a, b: a | b, def_depends.values()) - def_depends.keys()
        betas = {label: Beta(label, 0, None, None, 0) for label in beta_labels}

        # define alternatives in topological order to consider dependencies
        alternatives = {}
        availability_conditions = {}
        for label in TopologicalSorter(alternative_depends).static_order():
            alt = model.alternatives[label]
            alternatives[label] = alt.function.eval(**(db.variables | betas | alternatives))
            availability_conditions[label] = alt.availability_condition.eval(**db.variables)

        # define choice variable
        choice = model.choice.eval(**db.variables)

        prop = logit(dict(enumerate(alternatives.values(), start=1)),
                     dict(enumerate(availability_conditions.values(), start=1)),
                     choice)
        bio_model = BIOGEME(db, prop)
        bio_model.generate_html, bio_model.generate_pickle = False, False  # disable generating result files
        bio_model.modelName = 'biogeme_model'  # set model name to prevent warning from biogeme
        bio_result = bio_model.estimate()
        return Evaluation(bio_result.getEstimatedParameters())

    @property
    def display_name(self) -> str:
        return SingleLogitBiogemeConfig.__DISPLAY_NAME

    def set_settings(self, settings: dict[str, object]) -> SingleLogitBiogemeConfig:
        return SingleLogitBiogemeConfig(settings)
