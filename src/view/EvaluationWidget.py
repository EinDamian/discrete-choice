from __future__ import annotations
import os

from PyQt5.QtWidgets import QWidget, QTableView, QPushButton, QToolButton
from PyQt5 import uic

from src.controller.calculation.EvaluationController import EvaluationController
from src.model.processing.Threshold import Threshold

class EvaluationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/evaluation.ui', self)  # load ui file created with Qt Creator

        self.__controller: EvaluationController = EvaluationController()

    def update(self):
        super().update()

    def set_thresholds(self, thresholds: dict[str, Threshold]):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def evaluate(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def optimize(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def export(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def view_threshold_window(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
