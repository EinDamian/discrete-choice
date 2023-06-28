from __future__ import annotations

from PySide6.QtWidgets import QMainWindow

from src.view.ColumnWidget import ColumnWidget
from src.view.ModelWidget import ModelWidget
from src.view.ProcessingWidget import ProcessingWidget
from src.view.EvaluationWidget import EvaluationWidget
from src.view.FileMenu import FileMenu
from src.view.EditMenu import EditMenu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__columns: ColumnWidget = None
        self.__model: ModelWidget = None
        self.__processing_info: ProcessingWidget = None
        self.__evaluation: EvaluationWidget = None
        self.__file_menu: FileMenu = None
        self.__edit_menu: EditMenu = None

        #raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def update(self):
        pass#raise NotImplementedError  # TODO: IMPLEMENTIEREN
