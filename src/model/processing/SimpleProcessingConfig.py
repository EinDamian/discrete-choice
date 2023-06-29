from __future__ import annotations
from dataclasses import dataclass
import itertools

from src.model.data.Model import Model
from src.model.processing.ProcessingConfig import ProcessingConfig
from src.model.processing.Evaluation import Evaluation

import pandas as pd

@dataclass(frozen=True)
class SimpleProcessingConfig(ProcessingConfig):
    __DISPLAY_NAME = 'Simple Maximum-Likelihood Estimation (Biogeme)'

    def process(self, model: Model) -> Evaluation:
        import biogeme.database as bio_database
        import biogeme.biogeme as bio
        import biogeme.models as bio_models
        import biogeme.expressions as bio_expr

        # load raw data into biogeme database
        db = bio_database.Database('', model.data.raw_data)

        # define derivatives in biogeme database
        for label, e in model.data.derivatives.items():  # TODO: VERBESSERN UM Z.B. ZYKLEN UND ABHÄNGIGKEITEN IN ANDERER REIHENFOLGE ZU ERKENNEN
            db.DefineVariable(label, e.eval(**db.variables))

        # define beta variables in biogeme database
        alt_variables = set(itertools.chain.from_iterable(map(lambda e: e.variables, model.alternatives.values())))
        unused_variables = alt_variables - db.variables.keys()
        betas = {label: bio_expr.Beta(label, 0, None, None, 0) for label in unused_variables}  # unused variables in alternatives are interpreted as beta variables

        # define alternatives in biogeme database
        alternatives = {label: e.eval(**(db.variables | betas)) for label, e in model.alternatives.items()}

        av_cons = {}  # TODO: ???  # availability conditions?
        choice = 0  # TODO: ???  # choice?

        prop = bio_models.logit(alternatives, av_cons, choice)
        bio_model = bio.BIOGEME(db, prop)
        bio_model.generate_html, bio_model.generate_pickle = False, False  # disable generating result files
        bio_model.modelName = 'biogeme_model'  # set model name to prevent warning from biogeme
        result = bio_model.estimate()
        return Evaluation(result.getEstimatedParameters())

    @property
    def display_name(self) -> str:
        return SimpleProcessingConfig.__DISPLAY_NAME

    def set_settings(self, settings: pd.DataFrame) -> SimpleProcessingConfig:
        return SimpleProcessingConfig(settings)
