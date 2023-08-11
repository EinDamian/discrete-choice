from __future__ import annotations
import os

from src.model.processing.SingleLogitBiogemeConfig import SingleLogitBiogemeConfig
from src.model.processing.Evaluation import Evaluation
from src.model.data.Data import Data
from src.model.data.Model import Model
from src.model.data.Alternative import Alternative
from src.model.data.functions.FunctionalExpression import FunctionalExpression

import unittest
from parameterized import parameterized
import pandas as pd


class TestSingleLogitBiogemeConfig(unittest.TestCase):
    @staticmethod
    def __swissmetro_raw_data():
        raw_data = pd.read_csv(f'{os.path.dirname(__file__)}/../../resources/swissmetro.csv', sep='\t')
        raw_data = raw_data.drop(
            raw_data[((raw_data['PURPOSE'] != 1) * (raw_data['PURPOSE'] != 3) + (raw_data['CHOICE'] == 0)) > 0].index)
        return raw_data

    @staticmethod
    def __ifvrabus_raw_data():
        return pd.read_csv(f'{os.path.dirname(__file__)}/../../resources/Choicedata.csv', sep=';')

    @parameterized.expand([
        ('b01logit', Model(Data(raw_data=__swissmetro_raw_data(), raw_data_path=None,
                                derivatives={
                                    'SM_COST': FunctionalExpression('SM_CO * (GA == 0)'),
                                    'TRAIN_COST': FunctionalExpression('TRAIN_CO * (GA == 0)'),
                                    'CAR_AV_SP': FunctionalExpression('CAR_AV * (SP != 0)'),
                                    'TRAIN_AV_SP': FunctionalExpression('TRAIN_AV * (SP != 0)'),
                                    'TRAIN_TT_SCALED': FunctionalExpression('TRAIN_TT / 100'),
                                    'TRAIN_COST_SCALED': FunctionalExpression('TRAIN_COST / 100'),
                                    'SM_TT_SCALED': FunctionalExpression('SM_TT / 100'),
                                    'SM_COST_SCALED': FunctionalExpression('SM_COST / 100'),
                                    'CAR_TT_SCALED': FunctionalExpression('CAR_TT / 100'),
                                    'CAR_CO_SCALED': FunctionalExpression('CAR_CO / 100'),
                                }), alternatives={
            'alt1': Alternative(
                FunctionalExpression('ASC_TRAIN + B_TIME * TRAIN_TT_SCALED + B_COST * TRAIN_COST_SCALED'),
                availability_condition=FunctionalExpression('TRAIN_AV_SP'),
                choice_idx=1),
            'alt2': Alternative(
                FunctionalExpression('ASC_SM + B_TIME * SM_TT_SCALED + B_COST * SM_COST_SCALED'),
                availability_condition=FunctionalExpression('SM_AV'),
                choice_idx=2),
            'alt3': Alternative(
                FunctionalExpression('ASC_CAR + B_TIME * CAR_TT_SCALED + B_COST * CAR_CO_SCALED'),
                availability_condition=FunctionalExpression('CAR_AV_SP'),
                choice_idx=3)
        }, choice=FunctionalExpression('CHOICE'))),

        ('ifv_rabus',
         Model(Data(raw_data=__ifvrabus_raw_data(), raw_data_path=None, derivatives={}),
               alternatives={
                   'fuss': Alternative(
                       FunctionalExpression(
                           'asc_fuss + b_arbeit_on_fuss * (Wegezweck == 1) + b_freizeit_on_fuss * (Wegezweck == 4) + fz_fuss * bfz_fuss'),
                       availability_condition=FunctionalExpression('av_fuss'),
                       choice_idx=1),
                   'oev_fuss': Alternative(
                       FunctionalExpression(
                           'asc_oev_fuss + b_arbeit_on_oev_fuss * (Wegezweck == 1) + b_freizeit_on_oev_fuss * (Wegezweck == 4) + bfz_oev * fz_oev_fuss + bcost_oev * cost_oev_fuss + bfreq_oev * freq_oev_fuss + bfz_fuss2oev * zugang_oev_fuss'),
                       availability_condition=FunctionalExpression('av_oev_fuss'),
                       choice_idx=6),
                   'rad': Alternative(
                       FunctionalExpression(
                           'asc_rad + b_arbeit_on_rad * (Wegezweck == 1) + b_freizeit_on_rad * (Wegezweck == 4) + bfz_rad * fz_rad'),
                       availability_condition=FunctionalExpression('av_rad'),
                       choice_idx=2),
                   'car': Alternative(
                       FunctionalExpression(
                           'asc_car + b_arbeit_on_car * (Wegezweck == 1) + b_freizeit_on_car * (Wegezweck == 4) + bfz_car * fz_car'),
                       availability_condition=FunctionalExpression('av_car'),
                       choice_idx=4),
                   'shuttle_tb': Alternative(
                       FunctionalExpression(
                           'asc_shuttle_tb + b_oek1_on_shuttle_tb * (oek_status == 1) + b_arbeit_on_shuttle_tb * (Wegezweck == 1) + b_freizeit_on_shuttle_tb * (Wegezweck == 4) + bfz_shuttle * fz_shuttle_tb'),
                       availability_condition=FunctionalExpression('av_shuttle_tb'),
                       choice_idx=13),
                   'shuttle_od': Alternative(
                       FunctionalExpression(
                           'asc_shuttle_od + b_oek1_on_shuttle_od * (oek_status == 1) + b_arbeit_on_shuttle_od * (Wegezweck == 1) + b_freizeit_on_shuttle_od * (Wegezweck == 4) + bfz_shuttle * fz_shuttle_od'),
                       availability_condition=FunctionalExpression('av_shuttle_od'),
                       choice_idx=14),
                   'oev_rad': Alternative(
                       FunctionalExpression(
                           'asc_oev_rad + b_arbeit_on_oev_rad * (Wegezweck == 1) + b_freizeit_on_oev_rad * (Wegezweck == 4) + bfz_oev*Zeit_oev_rad'),
                       availability_condition=FunctionalExpression('av_oev_rad'),
                       choice_idx=7),
                   'oev_car': Alternative(
                       FunctionalExpression('asc_oev_car + bfz_oev*Zeit_oev_car'),
                       availability_condition=FunctionalExpression('av_oev_car'),
                       choice_idx=11),
                   'oev_shuttle_tb': Alternative(
                       FunctionalExpression(
                           'asc_oev_shuttle_tb + b_freizeit_on_oev_shuttle_tb * (Wegezweck == 4) + bfz_oev * Zeit_oev_shuttle_tb'),
                       availability_condition=FunctionalExpression('av_oev_shuttle_tb'),
                       choice_idx=9),
                   'oev_shuttle_od': Alternative(
                       FunctionalExpression(
                           'asc_oev_shuttle_od + b_freizeit_on_oev_shuttle_od * (Wegezweck == 4) + bfz_oev * Zeit_oev_shuttle_od'),
                       availability_condition=FunctionalExpression('av_oev_shuttle_od'),
                       choice_idx=10)
               }, choice=FunctionalExpression('choice'))),
    ])
    def test_process(self, name: str, model: Model):
        """
        Example for using biogeme.
        Source: https://github.com/michelbierlaire/biogeme/blob/master/examples/swissmetro/b01logit.py (06.07.2023)
        """
        config = SingleLogitBiogemeConfig()
        print(model.data.raw_data.columns)
        evaluation = config.process(model)

        self.assertEqual(type(evaluation.result), pd.DataFrame)

    @parameterized.expand([
        ('b01logit_missing_variable', KeyError,
         Model(Data(raw_data=__swissmetro_raw_data(), raw_data_path=None,
                    derivatives={
                        'SM_COST': FunctionalExpression('SM_CO * (GA == 0)'),
                        'CAR_AV_SP': FunctionalExpression('CAR_AV * (SP != 0)'),
                        'TRAIN_AV_SP': FunctionalExpression('TRAIN_AV * (SP != 0)'),
                        'TRAIN_TT_SCALED': FunctionalExpression('TRAIN_TT / 100'),
                        'TRAIN_COST_SCALED': FunctionalExpression('abc / 100'),
                        'SM_TT_SCALED': FunctionalExpression('SM_TT / 100'),
                        'SM_COST_SCALED': FunctionalExpression('SM_COST / 100'),
                        'CAR_TT_SCALED': FunctionalExpression('CAR_TT / 100'),
                        'CAR_CO_SCALED': FunctionalExpression('CAR_CO / 100'),
                    }), alternatives={
             'alt1': Alternative(
                 FunctionalExpression('ASC_TRAIN + B_TIME * TRAIN_TT_SCALED + B_COST * TRAIN_COST_SCALED'),
                 availability_condition=FunctionalExpression('TRAIN_AV_SP'),
                 choice_idx=1),
             'alt2': Alternative(
                 FunctionalExpression('ASC_SM + B_TIME * SM_TT_SCALED + B_COST * SM_COST_SCALED'),
                 availability_condition=FunctionalExpression('SM_AV'),
                 choice_idx=2),
             'alt3': Alternative(
                 FunctionalExpression('ASC_CAR + B_TIME * CAR_TT_SCALED + B_COST * CAR_CO_SCALED'),
                 availability_condition=FunctionalExpression('CAR_AV_SP'),
                 choice_idx=3)
         }, choice=FunctionalExpression('CHOICE'))),

        ('b01logit_cyclic_definition', KeyError,
         Model(Data(raw_data=__swissmetro_raw_data(), raw_data_path=None,
                    derivatives={
                        'SM_COST': FunctionalExpression('SM_CO * (GA == 0)'),
                        'TRAIN_COST': FunctionalExpression('TRAIN_COST_SCALED * (GA == 0)'),
                        'CAR_AV_SP': FunctionalExpression('CAR_AV * (SP != 0)'),
                        'TRAIN_AV_SP': FunctionalExpression('TRAIN_AV * (SP != 0)'),
                        'TRAIN_TT_SCALED': FunctionalExpression('TRAIN_TT / 100'),
                        'TRAIN_COST_SCALED': FunctionalExpression('TRAIN_COST / 100'),
                        'SM_TT_SCALED': FunctionalExpression('SM_TT / 100'),
                        'SM_COST_SCALED': FunctionalExpression('SM_COST / 100'),
                        'CAR_TT_SCALED': FunctionalExpression('CAR_TT / 100'),
                        'CAR_CO_SCALED': FunctionalExpression('CAR_CO / 100'),
                    }), alternatives={
             'alt1': Alternative(
                 FunctionalExpression('ASC_TRAIN + B_TIME * TRAIN_TT_SCALED + B_COST * TRAIN_COST_SCALED'),
                 availability_condition=FunctionalExpression('TRAIN_AV_SP'),
                 choice_idx=1),
             'alt2': Alternative(
                 FunctionalExpression('ASC_SM + B_TIME * SM_TT_SCALED + B_COST * SM_COST_SCALED'),
                 availability_condition=FunctionalExpression('SM_AV'),
                 choice_idx=2),
             'alt3': Alternative(
                 FunctionalExpression('ASC_CAR + B_TIME * CAR_TT_SCALED + B_COST * CAR_CO_SCALED'),
                 availability_condition=FunctionalExpression('CAR_AV_SP'),
                 choice_idx=3)
         }, choice=FunctionalExpression('CHOICE'))),

        ('b01logit_syntax', SyntaxError,
         Model(Data(raw_data=__swissmetro_raw_data(), raw_data_path=None,
                    derivatives={
                        'SM_COST': FunctionalExpression('SM_CO ****** (GA == 0)'),
                        'TRAIN_COST': FunctionalExpression('TRAIN_CO * (GA == 0)'),
                        'CAR_AV_SP': FunctionalExpression('CAR_AV * (SP != 0)'),
                        'TRAIN_AV_SP': FunctionalExpression('TRAIN_AV * (SP != 0)'),
                        'TRAIN_TT_SCALED': FunctionalExpression('TRAIN_TT / 100'),
                        'TRAIN_COST_SCALED': FunctionalExpression('TRAIN_COST / 100'),
                        'SM_TT_SCALED': FunctionalExpression('SM_TT / 100'),
                        'SM_COST_SCALED': FunctionalExpression('SM_COST / 100'),
                        'CAR_TT_SCALED': FunctionalExpression('CAR_TT / 100'),
                        'CAR_CO_SCALED': FunctionalExpression('CAR_CO / 100'),
                    }), alternatives={
             'alt1': Alternative(
                 FunctionalExpression('ASC_TRAIN + B_TIME * TRAIN_TT_SCALED + B_COST * TRAIN_COST_SCALED'),
                 availability_condition=FunctionalExpression('TRAIN_AV_SP'),
                 choice_idx=1),
             'alt2': Alternative(
                 FunctionalExpression('ASC_SM + B_TIME * SM_TT_SCALED + B_COST * SM_COST_SCALED'),
                 availability_condition=FunctionalExpression('SM_AV'),
                 choice_idx=2),
             'alt3': Alternative(
                 FunctionalExpression('ASC_CAR + B_TIME * CAR_TT_SCALED + B_COST * CAR_CO_SCALED'),
                 availability_condition=FunctionalExpression('CAR_AV_SP'),
                 choice_idx=3)
         }, choice=FunctionalExpression('CHOICE'))),
    ])
    def test_error_process(self, name: str, expected_exception, model: Model):
        """
        Example for using biogeme.
        Source: https://github.com/michelbierlaire/biogeme/blob/master/examples/swissmetro/b01logit.py (06.07.2023)
        """
        config = SingleLogitBiogemeConfig()

        with self.assertRaises(expected_exception):
            config.process(model)

    @staticmethod
    def __example__b01logit() -> Evaluation:
        """
        Example for using biogeme.
        Source: https://github.com/michelbierlaire/biogeme/blob/master/examples/swissmetro/b01logit.py (06.07.2023)
        """
        # %%
        import biogeme.biogeme as bio
        from biogeme import models
        from biogeme.expressions import Beta
        import pandas as pd
        import biogeme.database as db
        from biogeme.expressions import Variable
        # %%
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
        # %%
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

        availability_conditions = [
            TRAIN_AV_SP,
            SM_AV,
            CAR_AV_SP
        ]

        choice = database.variables['CHOICE']

        # %%
        prop = models.logit(dict(enumerate(v, 1)), availability_conditions, choice)

        # Create the Biogeme object
        bio_model = bio.BIOGEME(database, prop)
        bio_model.generate_html, bio_model.generate_pickle = False, False  # disable generating result files
        bio_model.modelName = 'biogeme_model'  # set model name to prevent warning from biogeme
        result = bio_model.estimate()
        print(result.getEstimatedParameters())
        # %%
        return Evaluation(result.getEstimatedParameters())


if __name__ == '__main__':
    unittest.main()
