from __future__ import annotations
import os

from PyQt5.QtCore import QSortFilterProxyModel, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QComboBox, QLineEdit, QTreeView, QAbstractItemView
from PyQt5 import uic

from src.controller.calculation.ConfigurationController import ConfigurationController
from src.view.FunctionHighlightDelegate import FunctionHighlightDelegate


class ProcessingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/processing_info.ui', self)  # load ui file created with Qt Creator

        self.__controller: ConfigurationController = ConfigurationController()

        # set up combo box
        self.combo_box = self.findChild(QComboBox, "combo_process_type")
        self.combo_box.currentTextChanged.connect(self.set_selected_config)

        # set the table with the events (changing and selecting) into the tree view
        self.__model = QStandardItemModel()

        # set up search bar
        self.__search_filter_proxy_model = QSortFilterProxyModel()
        self.__search_filter_proxy_model.setSourceModel(self.__model)
        self.__search_filter_proxy_model.setFilterCaseSensitivity(
            Qt.CaseInsensitive)
        self.__search_filter_proxy_model.setFilterKeyColumn(-1)
        self.__search_bar = self.findChild(QLineEdit, "search_field")
        self.__search_bar.textChanged.connect(
            self.__search_filter_proxy_model.setFilterRegExp)

        # add model to the treeview for the table
        self.__table = self.findChild(QTreeView, "table")
        self.__table.setModel(self.__search_filter_proxy_model)
        self.__table.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.__delegate = FunctionHighlightDelegate(parent=self.__table)
        self.__table.setItemDelegate(self.__delegate)
        self.__model.dataChanged.connect(self._data_changed)
        self.update()

    def update(self):
        # combo box update
        config_names = self.__controller.get_config_display_names()
        config_idx = 0  # TODO: GET CONFIG INDEX
        self.combo_box.clear()
        if config_names is not None:
            for name in config_names:
                self.combo_box.addItem(name)

        # clear the model for the tree view to add updated data
        self.__model.clear()
        self.__model.setHorizontalHeaderLabels(['Variable', 'Value'])

        # get the data from the model and add it to the table
        my_set = {"some", "random", "words", "in", "random", "order"}
        variables = my_set  # TODO: self.__controller.get_project().get_derivative_free_variables()
        for data in variables:
            row = []
            i = QStandardItem(str(data))
            i.setEditable(False)
            row.append(i)
            self.__model.appendRow(row)
        super().update()

    def set_selected_config(self):
        self.__controller.select_config(self.combo_process_type.currentIndex())

    def set_config_settings_item(self, variable: str, value: str):
        self.__controller.update_settings_item(variable, value)

    def _data_changed(self, top_left: QStandardItem, bottom_right: QStandardItem):
        """When a field is changed by the user this function is called to find the row that has been changed.

        Args:
            top_left (QStandardItem): _description_
            bottom_right (QStandardItem): _description_
        """
        for row in range(top_left.row(), bottom_right.row() + 1):
            for column in range(top_left.column(), bottom_right.column() + 1):
                self.__current_row = row
        variable = self.__model.item(self.__current_row).text()
        value = self.__model.item(self.__current_row, 1).text()
        self.set_config_settings_item(variable, value)
