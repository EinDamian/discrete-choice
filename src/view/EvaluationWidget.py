from __future__ import annotations
import os

from PyQt5.QtWidgets import QWidget, QPushButton, QToolButton
from PyQt5 import uic

from src.controller.calculation.EvaluationController import EvaluationController
from src.model.processing.Threshold import Threshold


class EvaluationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/evaluation.ui', self)  # load ui file created with Qt Creator

        self.__controller: EvaluationController = EvaluationController()

        calculateButton = self.findChild(QPushButton, "button_calculate")
        calculateButton.clicked.connect(self.evaluate)
        exportButton = self.findChild(QPushButton, "export_evaluation_button")
        exportButton.clicked.connect(self.export)
        optimizeButton = self.findChild(QPushButton, "update_model_button")
        optimizeButton.clicked.connect(self.optimize)
        viewOptionsButton = self.findChild(QToolButton, "view_options_button")
        viewOptionsButton.clicked.connect(self.view_threshold_window)

    def update(self):
        super().update()

    def set_thresholds(self, thresholds: dict[str, float]):
        for i in list(thresholds.values()):
            print(i)
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def evaluate(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def optimize(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def export(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def view_threshold_window(self):
        from src.view.ThresholdWindow import ThresholdWindow

        example = {'field1': 2,
                   'field2': 4.5,
                   'field3': 3}
        dialog = ThresholdWindow(example)
        dialog.show()
        dialog.applyClicked.connect(self.set_thresholds)
