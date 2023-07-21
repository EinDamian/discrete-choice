from __future__ import annotations

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMenu, QMenuBar

from src.view.Menu import Menu
from src.controller.ProjectManager import ProjectManager
from src.view.UIUtil import get_action


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

        self.redo_button = get_action(ui_edit_menu, 'action_redo')
        self.redo_button.triggered.connect(self.redo)

        self.undo_button = get_action(ui_edit_menu, 'action_undo')
        self.undo_button.triggered.connect(self.undo)

        self.update()

    def update(self):
        super().update()

        self.undo_button.setEnabled(self.__project_manager.can_undo())
        self.redo_button.setEnabled(self.__project_manager.can_redo())

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
