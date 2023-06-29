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
    def __init__(self):
        super().__init__()

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/main.ui', self)

        self.__columns: ColumnWidget = ColumnWidget(self.box_columns)
        self.__model: ModelWidget = ModelWidget(self.page_model)
        self.__processing_info: ProcessingWidget = ProcessingWidget(self.page_process)
        self.__evaluation: EvaluationWidget = EvaluationWidget(self.page_eval)
        #self.__file_menu: FileMenu = FileMenu(self)
        #self.__edit_menu: EditMenu = EditMenu(self)

    def update(self):
        super().update()
