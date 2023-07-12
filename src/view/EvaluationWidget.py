from __future__ import annotations
import os

import pandas
from PyQt5.QtWidgets import QWidget, QPushButton, QToolButton, QFileDialog, QTableView
from PyQt5 import uic

from src.controller.calculation.EvaluationController import EvaluationController
from src.view import DataFrameToModel


class EvaluationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/evaluation.ui', self)  # load ui file created with Qt Creator

        self.__controller: EvaluationController = EvaluationController()

        self.table = self.findChild(QTableView, "table")

        calculate_button = self.findChild(QPushButton, "button_calculate")
        calculate_button.clicked.connect(self.evaluate)
        export_button = self.findChild(QPushButton, "export_evaluation_button")
        export_button.clicked.connect(self.export)
        optimize_button = self.findChild(QPushButton, "update_model_button")
        optimize_button.setEnabled(False)
        optimize_button.clicked.connect(self.optimize)
        view_options_button = self.findChild(QToolButton, "view_options_button")
        view_options_button.clicked.connect(self.view_threshold_window)

    def update(self):
        super().update()

    def set_thresholds(self, thresholds: dict[str, float]):
        for i in list(thresholds.values()):
            print(i)
        '''Then We get the evaluation again(dataFram with highlighted cells) and assign it to self.table'''
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def evaluate(self):
        #self.__controller.evaluate()
        ''' if self.__controller.is_optimizable():
                self.optimize_button.setEnabled(True)'''
        #self.__controller.get_evaluation()

        data = {'Column1': [1, 2, 3, 4, 5],
                'Column2': ['A', 'B', 'C', 'D', 'E'],
                'Column3': [True, False, True, False, True]}
        df = pandas.DataFrame(data, index=['s1', 's2', 's3', 's4', 's5'])
        self.table.setModel(DataFrameToModel.DataFrameToModel(df))

        #raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def optimize(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def export(self):
        user_input = QFileDialog.getSaveFileName(self, 'Export File', '', 'Directory (*.dir)')
        if user_input:
            self.__controller.export(user_input[0])

    def view_threshold_window(self):
        from src.view.ThresholdWindow import ThresholdWindow

        example = {'field1': 2,
                   'field2': 4.5,
                   'field3': 3}
        dialog = ThresholdWindow(thresholds=example)
        dialog.setParent(self.parent().parent().parent())
        dialog.show()
        dialog.applyClicked.connect(self.set_thresholds)
        #raise NotImplementedError   #This code doesn't work, when i remove this
