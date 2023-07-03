from __future__ import annotations

from PyQt5.QtWidgets import QMenu, QFileDialog

from src.view.UIUtil import UIUtil
from src.view.Menu import Menu
from src.controller.ProjectManager import ProjectManager

class FileMenu(Menu):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__project_manager: ProjectManager = ProjectManager()

        ui_file_menu = self.parent().findChild(QMenu, "menu_file")

        new_project_button = UIUtil.get_action(ui_file_menu, 'action_new_project')
        new_project_button.triggered.connect(self.open_new_project)
        import_data_button = UIUtil.get_action(ui_file_menu, 'action_import_data')
        import_data_button.triggered.connect(self.import_data)
        open_project_button = UIUtil.get_action(ui_file_menu, 'action_project_open')
        open_project_button.triggered.connect(self.open_project)
        save_project_button = UIUtil.get_action(ui_file_menu, 'action_project_save')
        save_project_button.triggered.connect(self.save_project)
        save_as_button = UIUtil.get_action(ui_file_menu, 'action_project_save_as')
        save_as_button.triggered.connect(self.save_project_as)

    def open_project(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("JSON File (*.json)")
        if dlg.exec_():
            global filenames
            filenames = dlg.selectedFiles()
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def open_new_project(self):
        user_input = QFileDialog.getOpenFileName(self, 'Open New Project', '', 'Directory (*.dir)', )
        name = user_input[0] + '.json'
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def save_project(self):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def save_project_as(self):
        user_input = QFileDialog.getSaveFileName(self, 'Save File', '', 'Directory (*.dir)', )
        name = user_input[0] + '.json'
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def import_data(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("CSV File (*.csv)")
        if dlg.exec_():
            global filenames
            filenames = dlg.selectedFiles()
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def export_data(self):  #How to specify csv or JSON?
        user_input = QFileDialog.getSaveFileName(self, 'Export File', '', 'Directory (*.dir)', )
        name = user_input[0] + '.csv'
        raise NotImplementedError  # TODO: IMPLEMENTIEREN
