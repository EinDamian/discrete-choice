import os
import subprocess

from PyQt5.QtWidgets import QMenuBar, QMenu
from src.view.Menu import Menu
from src.view.UIUtil import get_action
from src.controller import ProjectManager
from pathlib import Path


class HelpMenu(Menu):
    """
    Represents the Help Menu in the GUI
    """

    def __init__(self, parent: QMenuBar):  # parent should be MenuBar
        """
        initializes a help menu by getting the GUI-Design and
        enabling the functionalities of the buttons
        @param parent: the parent of help menu
        @type parent: QMenuBar
        """
        super().__init__(parent)

        ui_help_menu = self.parent().findChild(QMenu, "menu_help")

        self.user_manual_button = get_action(ui_help_menu, 'action_user_manual')
        self.user_manual_button.triggered.connect(self.show_user_manual)
        self.project_manager = ProjectManager.ProjectManager()

    def show_user_manual(self):
        """
        performs the user's request to open the user manual
        """
        self.project_manager.open_user_manual()
