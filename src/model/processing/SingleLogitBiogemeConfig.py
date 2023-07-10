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

    @staticmethod
    def __example() -> Evaluation:
        """
        Example for using biogeme.
        Source: https://github.com/michelbierlaire/biogeme/blob/master/examples/swissmetro/b01logit.py (06.07.2023)
        """
        #%%
        import biogeme.biogeme as bio
        from biogeme import models
        from biogeme.expressions import Beta
        import pandas as pd
        import biogeme.database as db
        from biogeme.expressions import Variable
        #%%
        # Read the data
        df = pd.read_csv('src/test/resources/swissmetro.dat', sep='\t')
        database = db.Database('swissmetro', df)

        PURPOSE = Variable('PURPOSE')
        CHOICE = Variable('CHOICE')
        GA = Variable('GA')
        LUGGAGE = Variable('LUGGAGE')
        TRAIN_CO = Variable('TRAIN_CO')
        CAR_AV = Variable('CAR_AV')
        SP = Variable('SP')
        TRAIN_AV = Variable('TRAIN_AV')
        TRAIN_TT = Variable('TRAIN_TT')
        SM_TT = Variable('SM_TT')
        CAR_TT = Variable('CAR_TT')
        CAR_CO = Variable('CAR_CO')
        SM_CO = Variable('SM_CO')
        SM_AV = Variable('SM_AV')
        MALE = Variable('MALE')
        GROUP = Variable('GROUP')
        TRAIN_HE = Variable('TRAIN_HE')
        SM_HE = Variable('SM_HE')
        INCOME = Variable('INCOME')
        # Removing some observations can be done directly using pandas.
        # remove = (((database.data.PURPOSE != 1) &
        #           (database.data.PURPOSE != 3)) |
        #          (database.data.CHOICE == 0))
        # database.data.drop(database.data[remove].index,inplace=True)
        # Here we use the "biogeme" way:
        exclude = ((PURPOSE != 1) * (PURPOSE != 3) + (CHOICE == 0)) > 0
        database.remove(exclude)

        # Definition of new variables
        SM_COST = database.DefineVariable('SM_COST', SM_CO * (GA == 0))
        TRAIN_COST = database.DefineVariable('TRAIN_COST', TRAIN_CO * (GA == 0))
        CAR_AV_SP = database.DefineVariable('CAR_AV_SP', CAR_AV * (SP != 0))
        TRAIN_AV_SP = database.DefineVariable('TRAIN_AV_SP', TRAIN_AV * (SP != 0))
        TRAIN_TT_SCALED = database.DefineVariable('TRAIN_TT_SCALED', TRAIN_TT / 100)
        TRAIN_COST_SCALED = database.DefineVariable('TRAIN_COST_SCALED', TRAIN_COST / 100)
        SM_TT_SCALED = database.DefineVariable('SM_TT_SCALED', SM_TT / 100)
        SM_COST_SCALED = database.DefineVariable('SM_COST_SCALED', SM_COST / 100)
        CAR_TT_SCALED = database.DefineVariable('CAR_TT_SCALED', CAR_TT / 100)
        CAR_CO_SCALED = database.DefineVariable('CAR_CO_SCALED', CAR_CO / 100)
        #%%
        # Parameters to be estimated
        ASC_CAR = Beta('ASC_CAR', 0, None, None, 0)
        ASC_TRAIN = Beta('ASC_TRAIN', 0, None, None, 0)
        ASC_SM = Beta('ASC_SM', 0, None, None, 1)
        B_TIME = Beta('B_TIME', 0, None, None, 0)
        B_COST = Beta('B_COST', 0, None, None, 0)

        # Definition of the utility functions
        v = [
            ASC_TRAIN + B_TIME * TRAIN_TT_SCALED + B_COST * TRAIN_COST_SCALED,
            ASC_SM + B_TIME * SM_TT_SCALED + B_COST * SM_COST_SCALED,
            ASC_CAR + B_TIME * CAR_TT_SCALED + B_COST * CAR_CO_SCALED
        ]

        #%%
        prop = models.logit(dict(enumerate(v, 1)), None, database.variables['CHOICE'])

        # Create the Biogeme object
        bio_model = bio.BIOGEME(database, prop)
        bio_model.generate_html, bio_model.generate_pickle = False, False  # disable generating result files
        bio_model.modelName = 'biogeme_model'  # set model name to prevent warning from biogeme
        result = bio_model.estimate()
        print(result.getEstimatedParameters())
        #%%
        return Evaluation(result.getEstimatedParameters())

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
