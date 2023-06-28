from __future__ import annotations

from PySide6.QtWidgets import QMainWindow

from ColumnWidget import ColumnWidget
from ModelWidget import ModelWidget
from ProcessingWidget import ProcessingWidget
from EvaluationWidget import EvaluationWidget
from FileMenu import FileMenu
from EditMenu import EditMenu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__columns: ColumnWidget = None
        self.__model: ModelWidget = None
        self.__processing_info: ProcessingWidget = None
        self.__evaluation: EvaluationWidget = None
        self.__file_menu: FileMenu = None
        self.__edit_menu: EditMenu = None

        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def update(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
