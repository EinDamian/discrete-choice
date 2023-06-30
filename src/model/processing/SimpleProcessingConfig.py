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

    @staticmethod
    def __example() -> Evaluation:
        """Example for using biogeme. Source: https://www.youtube.com/watch?v=vS-Sg0htQP4 (30.06.2023)"""
        #%%
        import biogeme.database as bio_database
        import biogeme.biogeme as bio
        import biogeme.models as bio_models
        import biogeme.expressions as bio_expr
        import pandas as pd
        # %%
        # load raw data into biogeme database
        db = bio_database.Database('example', pd.read_csv('src/test/resources/swissmetro.dat', sep='\t'))
        # %%
        # define derivatives in biogeme database
        db.DefineVariable('SM_COST', db.variables['SM_CO'] * (db.variables['GA'] == 0))
        db.DefineVariable('TRAIN_COST', db.variables['TRAIN_CO'] * (db.variables['GA'] == 0))
        db.DefineVariable('CAR_AV_SP', db.variables['CAR_AV'] * (db.variables['SP'] == 0))
        db.DefineVariable('TRAIN_AV_SP', db.variables['TRAIN_AV'] * (db.variables['SP'] == 0))
        db.DefineVariable('TRAIN_TT_SCALED', db.variables['TRAIN_TT'] / 100)
        db.DefineVariable('TRAIN_COST_SCALED', db.variables['TRAIN_COST'] / 100)
        db.DefineVariable('SM_TT_SCALED', db.variables['SM_TT'] / 100)
        db.DefineVariable('SM_COST_SCALED', db.variables['SM_COST'] / 100)
        db.DefineVariable('CAR_TT_SCALED', db.variables['CAR_TT'] / 100)
        db.DefineVariable('CAR_CO_SCALED', db.variables['CAR_CO'] / 100)
        #%%
        # define beta variables in biogeme database
        ASC_CAR = bio_expr.Beta('ASC_CAR', 0, None, None, 0)
        ASC_TRAIN = bio_expr.Beta('ASC_TRAIN', 0, None, None, 0)
        ASC_SM = bio_expr.Beta('ASC_SM', 0, None, None, 1)
        B_TIME = bio_expr.Beta('B_TIME', 0, None, None, 0)
        B_COST = bio_expr.Beta('B_COST', 0, None, None, 0)
        #%%
        # define alternatives in biogeme database
        alternatives = [
            ASC_TRAIN + \
            B_TIME * db.variables['TRAIN_TT_SCALED'] + \
            B_COST * db.variables['TRAIN_COST_SCALED'],

            ASC_SM + \
            B_TIME * db.variables['SM_TT_SCALED'] + \
            B_COST * db.variables['SM_COST_SCALED'],

            ASC_CAR + \
            B_TIME * db.variables['CAR_TT_SCALED'] + \
            B_COST * db.variables['CAR_CO_SCALED']
        ]
        av_cons = [
            db.variables['TRAIN_AV_SP'],
            db.variables['SM_AV'],
            db.variables['CAR_AV_SP']
        ]
        choice = 0
        #%%
        prop = bio_models.logit({idx: val for idx, val in enumerate(alternatives)},
                                {idx: val for idx, val in enumerate(av_cons)},
                                choice)
        bio_model = bio.BIOGEME(db, prop)
        bio_model.generate_html, bio_model.generate_pickle = False, False  # disable generating result files
        bio_model.modelName = 'biogeme_model'  # set model name to prevent warning from biogeme
        result = bio_model.estimate()
        print(result.getEstimatedParameters())
        #%%
        return Evaluation(result.getEstimatedParameters())

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
        alternatives = [e.eval(**(db.variables | betas)) for label, e in model.alternatives.items()]
        av_cons = []  # TODO: ???  # availability conditions?
        choice = 1  # TODO: ???  # choice?

        prop = bio_models.logit({idx: val for idx, val in enumerate(alternatives)},
                                {idx: val for idx, val in enumerate(av_cons)},
                                choice)
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
