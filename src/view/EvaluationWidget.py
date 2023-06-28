from __future__ import annotations

from PySide6.QtWidgets import QWidget, QTableView, QPushButton, QToolButton

from ..controller.calculation.EvaluationController import EvaluationController
from ..model.processing.Threshold import Threshold

class EvaluationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.__table: QTableView = None
        self.__view_options_button: QToolButton = None
        self.__calculate_evaluation_button: QPushButton = None
        self.__update_model_button: QPushButton = None
        self.__export_evaluation_button: QPushButton = None
        self.__controller: EvaluationController = None

        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def update(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

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
