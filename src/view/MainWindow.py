from __future__ import annotations
import os
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

from src.view.ColumnWidget import ColumnWidget
from src.view.ModelWidget import ModelWidget
from src.view.ProcessingWidget import ProcessingWidget
from src.view.EvaluationWidget import EvaluationWidget
from src.view.FileMenu import FileMenu
from src.view.EditMenu import EditMenu


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/main.ui', self)  # load ui file created with Qt Creator

        # initiate all widgets at their correct positions
        self.__columns: ColumnWidget = ColumnWidget()
        self.layout_box_columns.setContentsMargins(0, 0, 0, 0)
        self.layout_box_columns.addWidget(self.__columns)

        self.__model: ModelWidget = ModelWidget()
        self.layout_page_model.setContentsMargins(0, 0, 0, 0)
        self.layout_page_model.addWidget(self.__model)

        self.__processing_info: ProcessingWidget = ProcessingWidget()
        self.layout_page_process.setContentsMargins(0, 0, 0, 0)
        self.layout_page_process.addWidget(self.__processing_info)

        self.__evaluation: EvaluationWidget = EvaluationWidget()
        self.layout_page_eval.setContentsMargins(0, 0, 0, 0)
        self.layout_page_eval.addWidget(self.__evaluation)

        self.__file_menu: FileMenu = FileMenu(parent=self.menuBar())    #The parent of a menu is the menuBar not the MainWindow
        self.__edit_menu: EditMenu = EditMenu(parent=self.menuBar())


    def update(self):
        super().update()
