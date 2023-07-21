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

        # initiate all widgets at their correct positions
        self.__columns: ColumnWidget = ColumnWidget()
        self.layout_box_columns.setContentsMargins(0, 0, 0, 0)
        self.layout_box_columns.addWidget(self.__columns)
        self.__columns.column_update_signal.connect(self.update)

        self.__model: ModelWidget = ModelWidget()
        self.layout_page_model.setContentsMargins(0, 0, 0, 0)
        self.layout_page_model.addWidget(self.__model)
        self.__model.model_update_signal.connect(self.update)

        self.__processing_info: ProcessingWidget = ProcessingWidget()
        self.layout_page_process.setContentsMargins(0, 0, 0, 0)
        self.layout_page_process.addWidget(self.__processing_info)
        self.__processing_info.processing_update_signal.connect(self.update)

        self.__evaluation: EvaluationWidget = EvaluationWidget()
        self.layout_page_eval.setContentsMargins(0, 0, 0, 0)
        self.layout_page_eval.addWidget(self.__evaluation)

        self.__file_menu: FileMenu = FileMenu(parent=self.menuBar())
        self.__file_menu.new_file_signal.connect(self.update)
        self.__edit_menu: EditMenu = EditMenu(parent=self.menuBar())
        self.__edit_menu.refresh_project_signal.connect(self.update)

    def update(self):
        super().update()

        self.__file_menu.update()
        self.__edit_menu.update()
        self.__columns.update()
        self.__model.update()
        self.__processing_info.update()
        self.__evaluation.update()
