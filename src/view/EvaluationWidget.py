from __future__ import annotations
import os
import sys

import pandas
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QPushButton, QToolButton, QFileDialog, QTableView, QStyledItemDelegate
from PyQt5 import uic

from src.controller.calculation.EvaluationController import EvaluationController
from src.view import DataFrameToModel
from src.view.HighlightingDelegate import HighlightingDelegate


class EvaluationWidget(QWidget):
    def __init__(self, parent=None, table_view=None):
        super().__init__(parent)

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/evaluation.ui', self)  # load ui file created with Qt Creator

        self.__controller: EvaluationController = EvaluationController()

        self.table = self.findChild(QTableView, "table")

        delegate = HighlightingDelegate()
        self.table.setItemDelegate(delegate)

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
        """Then We get the evaluation again(dataFrame) and assign it to self.table"""
        example_data = {'Column1': [1, 2, 3, 4, 5],
                        'Column2': [6, 7, 8, 9, 10],
                        'Column3': [11, 12, 13, 14, 15]}
        df = pandas.DataFrame(example_data, index=['s1', 's2', 's3', 's4', 's5'])
        self.table.setModel(DataFrameToModel.DataFrameToModel(df, thresholds))

    def evaluate(self):
        # self.__controller.evaluate()
        """ if self.__controller.is_optimizable():
                self.optimize_button.setEnabled(True)"""
        # df = self.__controller.get_evaluation()

        example_data = {'Column1': [1, 2, 3, 4, 5],
                        'Column2': [6, 7, 8, 9, 10],
                        'Column3': [11, 12, 13, 14, 15]}
        example_thresholds = {'Column1': 2,
                              'Column2': 4.5,
                              'Column3': 3}
        df = pandas.DataFrame(example_data, index=['s1', 's2', 's3', 's4', 's5'])
        self.table.setModel(DataFrameToModel.DataFrameToModel(df, thresholds=example_thresholds))

    def optimize(self):
        self.__controller.optimize()

    def export(self):
        user_input = QFileDialog.getSaveFileName(self, 'Export File', '', 'Directory (*.dir)')
        if user_input:
            self.__controller.export(user_input[0])

    def view_threshold_window(self):
        from src.view.ThresholdWindow import ThresholdWindow
        # curr_thresholds = self.__controller.get_thresholds()
        example = {'Column1': 2,
                   'Column2': 4.5,
                   'Column3': 3}
        dialog = ThresholdWindow(thresholds=example)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.applyClicked.connect(self.set_thresholds)
        dialog.exec_()
