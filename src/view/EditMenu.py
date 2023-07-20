from __future__ import annotations

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMenu, QMenuBar

from src.view.Menu import Menu
from src.controller.ProjectManager import ProjectManager
import src.view.UIUtil as UIUtil


class EditMenu(Menu):
    """
    This class represents the edit menu, which the one can find in the menu bar in the program
    """
    refresh_project_signal = pyqtSignal()

    def __init__(self, parent: QMenuBar):
        """
        Initializes the edit menu and adds the functionality
        @param parent: The menu bar, where the edit menu belongs
        @type parent: QMenuBar
        """
        super().__init__(parent)

        self.__project_manager: ProjectManager = ProjectManager()

        ui_edit_menu = self.parent().findChild(QMenu, "menu_edit")

        self.redo_button = UIUtil.get_action(ui_edit_menu, 'action_redo')
        self.redo_button.triggered.connect(self.redo)

        self.undo_button = UIUtil.get_action(ui_edit_menu, 'action_undo')
        self.undo_button.triggered.connect(self.undo)
        '''
        Remove these functions from edit menu?
        
        self.copy_button = UIUtil.get_action(ui_edit_menu, 'action_copy')
        self.copy_button.triggered.connect(self.copy)
        self.cut_button = UIUtil.get_action(ui_edit_menu, 'action_cut')
        self.cut_button.triggered.connect(self.cut)
        self.delete_button = UIUtil.get_action(ui_edit_menu, 'action_delete')
        self.delete_button.triggered.connect(self.delete)
        self.find_button = UIUtil.get_action(ui_edit_menu, 'action_find')
        self.find_button.triggered.connect(self.find)
        self.paste_button = UIUtil.get_action(ui_edit_menu, 'action_paste')
        self.paste_button.triggered.connect(self.paste)
        self.select_all_button = UIUtil.get_action(ui_edit_menu, 'action_select_all')
        self.select_all_button.triggered.connect(self.select_all)
        '''

    def cut(self, content: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def copy(self, content: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def paste(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def delete(self, content: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def find(self, content: str):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def select_all(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def undo(self):
        """
        Enables the user to perform 'undo'. The project will return to the previous state
        """
        self.__project_manager.undo()
        self.refresh_project_signal.emit()

    def redo(self):
        """
        Enables the user to perform 'redo'. The project will be updated to the next known state
        """
        self.__project_manager.redo()
        self.refresh_project_signal.emit()
