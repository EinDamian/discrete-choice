from __future__ import annotations

import os
import unittest

import pandas as pd

from src.config import ConfigExpressionErrors as Config
from src.model.ProjectSnapshot import ProjectSnapshot
from src.model.ProxyProject import ProxyProject
from src.model.SnapshotError import SnapshotError
from src.model.data.Alternative import Alternative
from src.model.data.Data import Data
from src.model.data.Model import Model
from src.model.data.functions.ErrorReport import ErrorReport
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.model.data.functions.StringMarker import StringMarker
from src.model.processing.ProcessingConfig import ProcessingConfig
from src.model.processing.SingleLogitBiogemeConfig import SingleLogitBiogemeConfig
from src.model.processing.Threshold import Threshold


class TestProxyProject(unittest.TestCase):
    def test_undo_redo(self):
        p = ProxyProject(ProjectSnapshot())
        self.assertFalse(p.can_undo())
        self.assertFalse(p.can_redo())

        d1 = {}
        d2 = {'A': FunctionalExpression('1')}

        p.set_derivatives(**d2)

        self.assertTrue(p.can_undo())
        self.assertFalse(p.can_redo())
        self.assertDictEqual(d2, p.get_derivatives())

        p.undo()

        self.assertFalse(p.can_undo())
        self.assertTrue(p.can_redo())
        self.assertDictEqual(d1, p.get_derivatives())

        p.redo()

        self.assertTrue(p.can_undo())
        self.assertFalse(p.can_redo())
        self.assertDictEqual(d2, p.get_derivatives())

    def test_path(self):
        snapshot = ProjectSnapshot(path="some_directory")
        proxy = ProxyProject(snapshot)
        self.assertEqual(proxy.path, "some_directory")

        proxy.set_path("new_directory")
        self.assertEqual(proxy.path, "new_directory")

    def test_configs(self):
        display_name = 'test_config_name'

        class TestConfig(ProcessingConfig):
            @property
            def display_name(self) -> str:
                return display_name

            def set_settings(self, settings: dict[str, FunctionalExpression]) -> TestConfig:
                return TestConfig(settings)

        config_1 = TestConfig({'a': FunctionalExpression("0")})
        config_2 = TestConfig({'b': FunctionalExpression("1")})
        index = 1
        snapshot = ProjectSnapshot(processing_configs=[config_1, config_2], selected_config_index=index)
        proxy = ProxyProject(snapshot)
        self.assertEqual(proxy.get_selected_config_index(), 1)
        self.assertEqual(proxy.get_config_settings(), [config_1.settings, config_2.settings])
        self.assertEqual(proxy.get_config_display_names(), [display_name, display_name])

        proxy.set_selected_config_index(0)

        proxy.undo()
        self.assertEqual(proxy.get_selected_config_index(), 1)
        proxy.redo()
        self.assertEqual(proxy.get_selected_config_index(), 0)

        proxy.set_config_settings(0, {'c': FunctionalExpression("2")})

        proxy.undo()
        self.assertEqual(proxy.get_config_settings(), [config_1.settings, config_2.settings])
        proxy.redo()
        self.assertEqual(proxy.get_config_settings(), [{'c': FunctionalExpression("2")}, config_2.settings])
        self.assertEqual(proxy.get_config_display_names(), [display_name, display_name])

    def test_evaluation(self):
        """
        Example for using biogeme.
        Source: https://github.com/michelbierlaire/biogeme/blob/master/examples/swissmetro/b01logit.py (06.07.2023)

        derivatives = {
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
        }

        alternatives = {
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
        }

        choice = FunctionalExpression('CHOICE')

        raw_data = pd.read_csv(f'{os.path.dirname(__file__)}/processing/../../resources/swissmetro.csv', sep='\t')
        raw_data = raw_data.drop(
            raw_data[((raw_data['PURPOSE'] != 1) * (raw_data['PURPOSE'] != 3) + (raw_data['CHOICE'] == 0)) > 0].index)
        data = Data(raw_data, None, derivatives)
        model = Model(data, alternatives, choice)
        config = SingleLogitBiogemeConfig()

        snapshot = ProjectSnapshot(model=model, processing_configs=[config], selected_config_index=0)
        proxy = ProxyProject(snapshot)
        proxy.evaluate()

        proxy.undo()
        self.assertEqual(proxy.get_evaluation(), None)
        proxy.redo()
        self.assertEqual(type(proxy.get_evaluation()), pd.DataFrame)
        print(proxy.get_evaluation())
        """

    def test_optimization(self):
        raise NotImplementedError

    def test_raw_data(self):
        snapshot = ProjectSnapshot()
        proxy = ProxyProject(snapshot)
        self.assertEqual(proxy.get_raw_data_path(), None)
        self.assertEqual(proxy.get_raw_data().empty, True)

        raw_data = pd.DataFrame(data={'col1': [1], 'col2': [-0.5]})
        model = Model(Data(raw_data=raw_data, raw_data_path="some_directory",
                           derivatives={}), alternatives={}, choice=FunctionalExpression(''))
        snapshot = ProjectSnapshot(model=model)
        proxy = ProxyProject(snapshot)
        self.assertEqual(proxy.get_raw_data_path(), "some_directory")
        self.assertEqual(proxy.get_raw_data().equals(raw_data), True)

        new_raw_data = pd.DataFrame(data={'col1': [2, 1], 'col2': [-0.25, None]})
        proxy.set_raw_data(data=new_raw_data, path="new_directory")

        proxy.undo()
        self.assertEqual(proxy.get_raw_data_path(), "some_directory")
        self.assertEqual(proxy.get_raw_data().equals(raw_data), True)
        proxy.redo()
        self.assertEqual(proxy.get_raw_data_path(), "new_directory")
        self.assertEqual(proxy.get_raw_data().equals(new_raw_data), True)

    def test_derivatives(self):
        snapshot = ProjectSnapshot()
        proxy = ProxyProject(snapshot)
        self.assertEqual(proxy.get_derivatives(), {})

        proxy.set_derivatives(**{'der': FunctionalExpression('0'),
                                 'der1': FunctionalExpression('0')})
        proxy.set_derivatives(**{'der1': FunctionalExpression('1'),
                                 'der2': FunctionalExpression('2'),
                                 'derx': FunctionalExpression('x')})

        proxy.undo()
        self.assertEqual(proxy.get_derivatives(), {'der': FunctionalExpression('0'), 'der1': FunctionalExpression('0')})
        proxy.redo()
        self.assertEqual(proxy.get_derivatives(), {'der': FunctionalExpression('0'),
                                                      'der1': FunctionalExpression('1'),
                                                      'der2': FunctionalExpression('2'),
                                                      'derx': FunctionalExpression('x')})

        proxy.remove_derivatives('der', 'der2')

        proxy.undo()
        self.assertEqual(proxy.get_derivatives(), {'der': FunctionalExpression('0'),
                                                   'der1': FunctionalExpression('1'),
                                                   'der2': FunctionalExpression('2'),
                                                   'derx': FunctionalExpression('x')})
        proxy.redo()
        self.assertEqual(proxy.get_derivatives(), {'der1': FunctionalExpression('1'),
                                                      'derx': FunctionalExpression('x')})

        self.assertEqual(proxy.get_derivative_error_report('der1'),
                         ErrorReport(True, set()))
        self.assertEqual(proxy.get_derivative_error_report('derx'),
                         ErrorReport(False, {StringMarker(Config.ERROR_VARIABLE_NON_EXISTENT.format('x'), 0, 1, Config.COLOR_HEX)}))
        with self.assertRaises(SnapshotError):
            proxy.get_derivative_error_report('der')
        self.assertEqual(proxy.get_derivative_type('der1'), int)
        with self.assertRaises(SnapshotError):
            proxy.get_derivative_type('derx')
        with self.assertRaises(SnapshotError):
            proxy.get_derivative_type('der')

        proxy.set_derivatives(**{'der': FunctionalExpression('a * 2 + der1 / y - z')})
        self.assertEqual(proxy.get_derivative_free_variables(), {'a', 'x', 'y', 'z'})

        proxy.set_raw_data(data=pd.DataFrame({'a': [1, 2]}), path="some_path")
        proxy.set_derivatives(**{'z': FunctionalExpression('der1')})
        proxy.set_alternatives(**{'x': 2})
        proxy.set_config_settings(0, {'x': 1})
        self.assertEqual(proxy.get_derivative_free_variables(), {'x', 'y'})

    def test_alternatives(self):
        snapshot = ProjectSnapshot()
        proxy = ProxyProject(snapshot)
        self.assertEqual(proxy.get_alternatives(), {})

        proxy.set_alternatives(**{'alt': Alternative(function=FunctionalExpression('0'),
                                                        availability_condition=FunctionalExpression('1'),
                                                        choice_idx=0),
                                  'alt1': Alternative(function=FunctionalExpression('0'),
                                                     availability_condition=FunctionalExpression('1'),
                                                     choice_idx=0)})
        proxy.set_alternatives(**{'alt1': Alternative(function=FunctionalExpression('1'),
                                                         availability_condition=FunctionalExpression('1'),
                                                         choice_idx=0),
                                     'alt2': Alternative(function=FunctionalExpression('2'),
                                                         availability_condition=FunctionalExpression('1'),
                                                         choice_idx=0),
                                     'altx': Alternative(function=FunctionalExpression('x'),
                                                         availability_condition=FunctionalExpression('z'),
                                                         choice_idx=0)})

        proxy.undo()
        self.assertEqual(proxy.get_alternatives(), {'alt': Alternative(function=FunctionalExpression('0'),
                                                                       availability_condition=FunctionalExpression('1'),
                                                                       choice_idx=0),
                                                    'alt1': Alternative(function=FunctionalExpression('0'),
                                                                        availability_condition=FunctionalExpression(
                                                                            '1'),
                                                                        choice_idx=0)})
        proxy.redo()
        self.assertEqual(proxy.get_alternatives(), {'alt': Alternative(function=FunctionalExpression('0'),
                                                                          availability_condition=FunctionalExpression('1'),
                                                                          choice_idx=0),
                                                       'alt1': Alternative(function=FunctionalExpression('1'),
                                                                           availability_condition=FunctionalExpression('1'),
                                                                           choice_idx=0),
                                                       'alt2': Alternative(function=FunctionalExpression('2'),
                                                                           availability_condition=FunctionalExpression('1'),
                                                                           choice_idx=0),
                                                       'altx': Alternative(function=FunctionalExpression('x'),
                                                                           availability_condition=FunctionalExpression('z'),
                                                                           choice_idx=0)})

        proxy.remove_alternatives('alt', 'alt2')

        proxy.undo()
        self.assertEqual(proxy.get_alternatives(), {'alt': Alternative(function=FunctionalExpression('0'),
                                                                       availability_condition=FunctionalExpression('1'),
                                                                       choice_idx=0),
                                                    'alt1': Alternative(function=FunctionalExpression('1'),
                                                                        availability_condition=FunctionalExpression(
                                                                            '1'),
                                                                        choice_idx=0),
                                                    'alt2': Alternative(function=FunctionalExpression('2'),
                                                                        availability_condition=FunctionalExpression(
                                                                            '1'),
                                                                        choice_idx=0),
                                                    'altx': Alternative(function=FunctionalExpression('x'),
                                                                        availability_condition=FunctionalExpression(
                                                                            'z'),
                                                                        choice_idx=0)})
        proxy.redo()
        self.assertEqual(proxy.get_alternatives(), {'alt1': Alternative(function=FunctionalExpression('1'),
                                                                           availability_condition=FunctionalExpression('1'),
                                                                           choice_idx=0),
                                                       'altx': Alternative(function=FunctionalExpression('x'),
                                                                           availability_condition=FunctionalExpression('z'),
                                                                           choice_idx=0)})
        self.assertEqual(proxy.get_alternative_error_report('altx'),
                         ErrorReport(False, {StringMarker(Config.ERROR_VARIABLE_NON_EXISTENT.format('x'), 0, 1, Config.COLOR_HEX)}))
        with self.assertRaises(SnapshotError):
            proxy.get_alternative_error_report('alt')
        self.assertEqual(proxy.get_availability_condition_error_report('altx'),
                         ErrorReport(False, {StringMarker(Config.ERROR_VARIABLE_NON_EXISTENT.format('z'), 0, 1, Config.COLOR_HEX)}))
        with self.assertRaises(SnapshotError):
            proxy.get_availability_condition_error_report('alt')

    def test_choice(self):
        snapshot = ProjectSnapshot()
        proxy = ProxyProject(snapshot)
        self.assertEqual(proxy.get_choice(), FunctionalExpression(''))

        model = Model(choice=FunctionalExpression('some_choice'),
                      alternatives={}, data=Data(pd.DataFrame(data={}), None, {}))
        snapshot = ProjectSnapshot(model=model)
        proxy = ProxyProject(snapshot)
        self.assertEqual(proxy.get_choice(), FunctionalExpression('some_choice'))

        proxy.set_choice(FunctionalExpression('new_choice'))

        proxy.undo()
        self.assertEqual(proxy.get_choice(), FunctionalExpression('some_choice'))
        proxy.redo()
        self.assertEqual(proxy.get_choice(), FunctionalExpression('new_choice'))

    def test_thresholds(self):
        snapshot = ProjectSnapshot()
        proxy = ProxyProject(snapshot)
        self.assertEqual(proxy.get_thresholds(), {})

        thresh1 = Threshold(value=1)
        snapshot = ProjectSnapshot(thresholds={'thresh1': thresh1})
        proxy = ProxyProject(snapshot)
        self.assertEqual(proxy.get_thresholds(), {'thresh1': Threshold(value=1)})

        thresh1 = Threshold(value=0.5)
        thresh2 = Threshold(value=100)
        proxy.set_thresholds(**{'thresh1': thresh1, 'thresh2': thresh2})

        proxy.undo()
        self.assertEqual(proxy.get_thresholds(), {'thresh1': Threshold(value=1)})
        proxy.redo()
        self.assertEqual(proxy.get_thresholds(), {'thresh1': thresh1, 'thresh2': thresh2})


if __name__ == '__main__':
    unittest.main()
