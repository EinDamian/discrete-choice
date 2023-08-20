from __future__ import annotations
import os

from src.model.processing.VariedLogitBiogemeConfig import VariedLogitBiogemeConfig
from src.model.processing.Evaluation import Evaluation
from src.model.data.Data import Data
from src.model.data.Model import Model
from src.model.data.Alternative import Alternative
from src.model.data.functions.FunctionalExpression import FunctionalExpression

import unittest
from parameterized import parameterized
import pandas as pd


class TestVariedLogitBiogemeConfig(unittest.TestCase):
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
        ('b01logit', {'x': 'range(2)', 'y': '0'},
         Model(Data(raw_data=__swissmetro_raw_data(), raw_data_path=None,
                    derivatives={
                        'SM_COST': FunctionalExpression('SM_CO * (GA == x)'),
                        'TRAIN_COST': FunctionalExpression('TRAIN_CO * (GA == y)'),
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
         }, choice=FunctionalExpression('CHOICE')), 2)
    ])
    def test_process(self, name: str, settings: dict[str, str], model: Model, expected_variations: int):
        """
        Example for using biogeme.
        Source: https://github.com/michelbierlaire/biogeme/blob/master/examples/swissmetro/b01logit.py (06.07.2023)
        """
        config = VariedLogitBiogemeConfig({k: FunctionalExpression(v) for k, v in settings.items()})
        evaluation = config.process(model)

        self.assertEqual(type(evaluation.result), pd.DataFrame)

        variations_count = len(set(evaluation.result.columns.get_level_values(0)))
        self.assertEqual(variations_count, expected_variations)


if __name__ == '__main__':
    unittest.main()
