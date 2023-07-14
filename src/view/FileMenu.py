from __future__ import annotations

from PyQt5.QtWidgets import QMenu, QFileDialog

from src.view.UIUtil import UIUtil
from src.view.Menu import Menu
from src.controller.ProjectManager import ProjectManager


class FileMenu(Menu):
    """
    This class represents the file menu in the main window. It enables the user to manage the project
    (create, open, save) and to import and export the data (csv contains survey data and derivatives)
    """
    def __init__(self, parent=None):    # parent should be MenuBar
        """
        initializes a file menu by getting the GUI-Design and
        enabling the functionalities of the buttons
        @param parent: the parent of file menu
        @type parent: QWidget
        """
        super().__init__(parent)

        self.__project_manager: ProjectManager = ProjectManager()

        ui_file_menu = self.parent().findChild(QMenu, "menu_file")

        self.new_project_button = UIUtil.get_action(ui_file_menu, 'action_new_project')
        self.new_project_button.triggered.connect(self.open_new_project)
        self.open_project_button = UIUtil.get_action(ui_file_menu, 'action_project_open')
        self.open_project_button.triggered.connect(self.open_project)
        self.save_project_button = UIUtil.get_action(ui_file_menu, 'action_project_save')
        self.save_project_button.triggered.connect(self.save_project)
        self.save_as_button = UIUtil.get_action(ui_file_menu, 'action_project_save_as')
        self.save_as_button.triggered.connect(self.save_project_as)
        self.import_data_button = UIUtil.get_action(ui_file_menu, 'action_import_data')
        self.import_data_button.triggered.connect(self.import_data)
        self.export_data_button = UIUtil.get_action(ui_file_menu, 'action_export_data')
        self.export_data_button.triggered.connect(self.export_data)

    def open_project(self):
        """
        Enables the user to open a project, which already exists.
        A File Dialog will be shown, where the user can only choose a directory,
        because a project can only be saved as directory
        """
        dlg = QFileDialog()
        dlg.setOption(QFileDialog.DontUseNativeDialog)
        dlg.setWindowTitle("Open Project")
        dlg.setFileMode(QFileDialog.DirectoryOnly)
        dlg.setNameFilter("Directory (*.dir)")
        dlg.exec_()
        dlg.fileSelected.connect(self.__project_manager.open)

    def open_new_project(self):
        """
        Enables the user to open a new project. The user can enter the project's path
        as soon as he tries to save it
        @return:
        @rtype:
        """
        # TODO: self.save_project() ?
        self.__project_manager.new()

    def save_project(self):
        """
        enables th user to save the opened project.
        In case the project is new and hasn't been saved before, a
        file dialog will be shown for choosing a path to save to.
        Otherwise, save is performed automatically.
        """
        if self.__project_manager.get_project().path is None:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            user_input = QFileDialog.getSaveFileName(self, 'Save File', '', 'Directory (*.dir)', options=options)
            if user_input:
                # self.__project_manager.get_project().path = user_input[0] #TODO need a setter in controller?
                self.__project_manager.save(None)
        else:
            self.__project_manager.save(None)

    def save_project_as(self):
        """
        enables the user to save the project in a path, that differs from the project's original path
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        user_input = QFileDialog.getSaveFileName(self, 'Save Project As', '', 'Directory (*.dir)', options=options)
        if user_input:
            self.__project_manager.save(user_input[0])  # user_input[0] contains the path

    def import_data(self):
        """
        Using this option in FileMenu, the user can import the survey data, which are stored in a csv file.
        """
        dlg = QFileDialog()
        dlg.setOption(QFileDialog.DontUseNativeDialog)
        dlg.setWindowTitle("Import Data")
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilter("CSV File (*.csv)")
        dlg.exec_()
        dlg.fileSelected.connect(self.__project_manager.import_)

    def export_data(self):  # TODO how to specify file type? csv, JSON?
        """
        This option enables the user to export the survey data and their derivatives to a path of  his choice.
        In the file dialog the user can name the exported file as he wishes.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        user_input = QFileDialog.getSaveFileName(self, 'Export to', '', 'Directory (*.dir)', options=options)
        if user_input:
            self.__project_manager.export(user_input[0])  # user_input[0] contains the path
