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
        db = Database('biogeme_model_db',
                      model.data.complete_data.select_dtypes(exclude=['object']).dropna(axis=1, how='any'))

        alt_depends = {label: alt.function.variables for label, alt in model.alternatives.items()}

        # define beta variables in biogeme database
        # undefined labels in alternatives are interpreted as beta variables
        beta_labels = functools.reduce(lambda a, b: a | b, alt_depends.values(), set()) - db.variables.keys()
        betas = {label: Beta(label, 0, None, None, 0) for label in beta_labels}

        # define alternatives in topological order to consider dependencies
        alts = {}
        av_conditions = {}
        for label in TopologicalSorter(alt_depends).static_order():
            if label in model.alternatives:
                alt = model.alternatives[label]
                try:
                    res_f = alt.function.eval(**(db.variables | alts | betas))
                except Exception as e:
                    raise ValueError(f'expression evaluation error ("{label}")') from e
                alts[label] = res_f
                try:
                    res_ac = alt.availability_condition.eval(**db.variables)
                except Exception as e:
                    raise ValueError(f'expression evaluation error (availability condition of "{label}")') from e
                av_conditions[label] = res_ac

        # define choice variable
        try:
            choice = model.choice.eval(**db.variables)
        except Exception as e:
            raise ValueError(f'expression evaluation error (choice)') from e

        def __map_alt_ids(alternatives):
            return {model.alternatives[label].choice_idx: val for label, val in alternatives.items()}

        prop = logit(__map_alt_ids(alts),
                     __map_alt_ids(av_conditions),
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
