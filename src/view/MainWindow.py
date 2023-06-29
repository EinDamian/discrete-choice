from __future__ import annotations
import os

from PyQt5.QtWidgets import QMainWindow
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

        # initiate widget at their correct positions
        self.__columns: ColumnWidget = ColumnWidget(parent=self.box_columns)
        self.__model: ModelWidget = ModelWidget(parent=self.page_model)
        self.__processing_info: ProcessingWidget = ProcessingWidget(parent=self.page_process)
        self.__evaluation: EvaluationWidget = EvaluationWidget(parent=self.page_eval)
        #self.__file_menu: FileMenu = FileMenu(parent=self)
        #self.__edit_menu: EditMenu = EditMenu(parent=self)

    def update(self):
        super().update()
