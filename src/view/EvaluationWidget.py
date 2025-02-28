from __future__ import annotations
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QToolButton, QTableView, QMessageBox
from PyQt5 import uic

from src.controller.calculation.EvaluationController import EvaluationController
from src.view.ThresholdWindow import ThresholdWindow
from src.view.DataFrameToTableModel import DataFrameToTableModel
from src.view.CellColoringDelegate import CellColoringDelegate
from src.config import ConfigEvaluationWidget as Cfg
from src.view.FileManagementWindow import FileManagementWindow
from src.view.UIUtil import display_exceptions


class EvaluationWidget(QWidget):
    """
    This class represents the evaluation widget in the GUI,
    where the user can request to evaluate the functions and export them.
    The user can also set thresholds or optimize the model
    """

    def __init__(self, parent=None):
        """
        Initializes a new evaluation widget.
        It means the graphics will be displayed, the functionalities of the buttons and other
        graphical elements (table) will be defined
        @param parent: The parent of the evaluation widget
        @type parent: QWidget
        """
        super().__init__(parent)

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/evaluation.ui', self)  # load ui file created with Qt Creator

        self.__controller: EvaluationController = EvaluationController()

        self.table = self.findChild(QTableView, "table")

        delegate = CellColoringDelegate()
        self.table.setItemDelegate(delegate)

        self.calculate_button = self.findChild(QPushButton, "button_calculate")
        self.calculate_button.clicked.connect(self.evaluate)
        self.export_button = self.findChild(QPushButton, "export_evaluation_button")
        self.export_button.clicked.connect(self.export)
        self.export_button.setEnabled(False)  # Because at the beginning there are no results to export
        self.optimize_button = self.findChild(QPushButton, "update_model_button")
        self.optimize_button.setEnabled(False)  # by default, the model cannot be optimized at the beginning
        self.optimize_button.clicked.connect(self.optimize)
        self.view_options_button = self.findChild(QToolButton, "view_options_button")
        self.view_options_button.setEnabled(False)  # At the beginning there is no evaluation and therefore no columns
        self.view_options_button.clicked.connect(self.view_threshold_window)

    def display_evaluation(self):
        """
        This function displays the evaluation.
        """
        evaluation = self.__controller.get_evaluation()
        thresholds = self.__controller.get_thresholds()
        if evaluation is None:
            self.table.setModel(None)
            self.export_button.setEnabled(False)
            self.view_options_button.setEnabled(False)
            self.optimize_button.setEnabled(False)
        else:
            table_model = DataFrameToTableModel(evaluation.round(3), thresholds=thresholds)
            self.table.setModel(table_model)
            self.export_button.setEnabled(True)
            self.view_options_button.setEnabled(True)

    def update(self):
        """
        refreshes (updates) the evaluation widget.
        More Specifically, the table in the widget
        """
        super().update()
        self.display_evaluation()

    def set_thresholds(self, thresholds: dict[str, float]):
        """
        This function is called by view_threshold_window() in order to pass the new values to the model
        and apply them on the recent evaluation
        @param thresholds: contains the name of columns and their thresholds
        @type thresholds: a dictionary, where the keys are the columns and their values are the thresholds
        """
        if thresholds != {}:
            self.__controller.set_thresholds(thresholds)
            self.display_evaluation()

    @display_exceptions
    def evaluate(self):
        """
        This function sends a request for evaluation to the controller.
        Then it gets the results and displays them to the user.
        The displaying occurs by automatically calling update()
        """
        
        # Info window that calculation is happening
        progress_dialog = QMessageBox(self)
        progress_dialog.setWindowTitle(Cfg.TEXT_CALCULATION)
        progress_dialog.setStandardButtons(QMessageBox.NoButton) 
        progress_dialog.setText(Cfg.TEXT_CALCULATION)
        progress_dialog.open()
        
        try:
            self.__controller.evaluate()
            self.optimize_button.setEnabled(self.__controller.is_optimizable())
            self.display_evaluation()
            progress_dialog.hide()
        except Exception as e:
            progress_dialog.hide()
            raise e

    def optimize(self):
        """
        This function is used to optimize the model after performing the evaluation
        """
        self.__controller.optimize()

    @display_exceptions
    def export(self):
        """
        This enables the user to export the results to a path of his/her choice
        """
        path = FileManagementWindow().save_file(Cfg.EXPORT_DIALOG_TITLE, Cfg.CSV_FILE_FORMAT)
        if path:
            self.__controller.export(path)

    def view_threshold_window(self):
        """
        This function creates  a new threshold window, where the user can enter the new thresholds
        """
        curr_thresholds = self.__controller.get_thresholds()
        dialog = ThresholdWindow(thresholds=curr_thresholds)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.applyClicked.connect(self.set_thresholds)
        dialog.exec_()
