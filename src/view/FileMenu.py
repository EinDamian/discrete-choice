from __future__ import annotations

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMenu, QFileDialog, QMenuBar

from src.view.UIUtil import get_action
from src.view.Menu import Menu
from src.controller.ProjectManager import ProjectManager
from src.controller.FileManager import FileManager
from src.config import ConfigFileMenu as Cfg
from src.view.MessageDialog import MessageDialog

from src.view.FileManagementWindow import FileManagementWindow


class FileMenu(Menu):
    """
    This class represents the file menu in the main window. It enables the user to manage the project
    (create, open, save) and to import and export the data (csv contains survey data and derivatives)

    the new_file_signal is the emitted signal, when a new project or csv file has been opened.
    """
    new_file_signal = pyqtSignal()

    def __init__(self, parent: QMenuBar):  # parent should be MenuBar
        """
        initializes a file menu by getting the GUI-Design and
        enabling the functionalities of the buttons
        @param parent: the parent of file menu
        @type parent: QMenuBar
        """
        super().__init__(parent)

        self.__project_manager: ProjectManager = ProjectManager()

        ui_file_menu = self.parent().findChild(QMenu, "menu_file")

        self.new_project_button = get_action(ui_file_menu, 'action_new_project')
        self.new_project_button.triggered.connect(self.open_new_project)
        self.open_project_button = get_action(ui_file_menu, 'action_project_open')
        self.open_project_button.triggered.connect(self.open_project)
        self.save_project_button = get_action(ui_file_menu, 'action_project_save')
        self.save_project_button.triggered.connect(self.save_project)
        self.save_as_button = get_action(ui_file_menu, 'action_project_save_as')
        self.save_as_button.triggered.connect(self.save_project_as)
        self.import_data_button = get_action(ui_file_menu, 'action_import_data')
        self.import_data_button.triggered.connect(self.import_data)
        self.export_data_button = get_action(ui_file_menu, 'action_export_data')
        self.export_data_button.triggered.connect(self.export_data)

    def open_project(self):
        """
        Enables the user to open a project, which already exists.
        A File Dialog will be shown, where the user can only choose a directory,
        because a project can only be saved as directory
        """
        if self.__project_manager.get_project() is not None:
            msg_dlg = MessageDialog(Cfg.WARNING_DIALOG_TITLE, Cfg.MESSAGE_DIALOG_SAVE_BEFORE_OTHER)
            if msg_dlg.get_decision():
                self.save_project()
        path = FileManagementWindow().open_file(Cfg.OPEN_PROJECT_DIALOG_TITLE,
                                                QFileDialog.DirectoryOnly,
                                                None)
        if path:
            self.__project_manager.open(path)
            self.new_file_signal.emit()

    def open_new_project(self):
        """
        Enables the user to open a new project. The user can enter the project's path
        as soon as he tries to save it
        """
        if self.__project_manager.get_project() is not None:
            msg_dlg = MessageDialog(Cfg.WARNING_DIALOG_TITLE, Cfg.MESSAGE_DIALOG_SAVE_BEFORE_NEW)
            if msg_dlg.get_decision():
                self.save_project()
        self.__project_manager.new()
        self.new_file_signal.emit()

    def save_project(self):
        """
        enables th user to save the opened project.
        In case the project is new and hasn't been saved before, a
        file dialog will be shown for choosing a path to save to.
        Otherwise, save is performed automatically.
        """
        if self.__project_manager.get_project().path is None:
            new_path = FileManagementWindow().save_file(Cfg.SAVE_PROJECT_DIALOG_TITLE, Cfg.DIRECTORY_FILE_FORMAT)
            if new_path:
                self.__project_manager.set_project_path(new_path)
                self.__project_manager.save(None)
        else:
            self.__project_manager.save(None)

    def save_project_as(self):
        """
        enables the user to save the project in a path, that differs from the project's original path
        """
        path = FileManagementWindow().save_file(Cfg.SAVE_PROJECT_AS_DIALOG_TITLE, Cfg.DIRECTORY_FILE_FORMAT)
        if path:
            self.__project_manager.save(path)

    def import_data(self):  # TODO Empfehlung
        """
        Using this option in FileMenu, the user can import the survey data, which are stored in a csv file.
        """
        path = FileManagementWindow().open_file(Cfg.IMPORT_DATA_DIALOG_TITLE,
                                                QFileDialog.ExistingFile, Cfg.CSV_FILE_FORMAT)
        if path:
            self.__project_manager.import_raw_data(path)
            self.new_file_signal.emit()


    def export_data(self):  # TODO how to specify file type? csv, JSON?
        """
        This option enables the user to export the survey data and their derivatives to a path of  his choice.
        In the file dialog the user can name the exported file as he wishes.
        """
        path = FileManagementWindow().save_file(Cfg.EXPORT_DATA_DIALOG_TITLE, Cfg.DIRECTORY_FILE_FORMAT)
        if path:
            self.__project_manager.export(path)  # TODO export fehlt im Controller?
