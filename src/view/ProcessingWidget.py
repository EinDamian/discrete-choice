from __future__ import annotations
import os

from PyQt5.QtCore import QSortFilterProxyModel, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QComboBox, QLineEdit, QTreeView, QAbstractItemView
from PyQt5 import uic

from src.controller.calculation.ConfigurationController import ConfigurationController
from src.view.HighlightDelegate import HighlightDelegate


class ProcessingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/processing_info.ui', self)  # load ui file created with Qt Creator

        self.__controller: ConfigurationController = ConfigurationController()

        # set up combo box
        self.combo_box = self.findChild(QComboBox, "combo_process_type")
        config_names = self.__controller.get_config_display_names()
        if config_names is not None:
            for name in config_names:
                self.combo_box.addItem(name)
        """self.combo_box.currentTextChanged.connect(self.set_selected_config)"""

        # set the table with the events (changing and selecting) into the tree view
        self.__model = QStandardItemModel()
        self.__model.dataChanged.connect(self._handle_data_changed)

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
        self.__table.selectionModel().selectionChanged.connect(
            self._handle_selection_change)

        self.__delegate = HighlightDelegate(parent=self.__table)
        self.__table.setItemDelegate(self.__delegate)

        self.update()

    def update(self):
        super().update()

        # clear the model for the tree view to add updated data
        self.__model.clear()
        self.__model.setHorizontalHeaderLabels(['Variable', 'Type', 'Value'])

        # get the data from the model and add it to the table
        mylist1 = ["%ag1min", "int", "10"]
        mylist2 = ["%ag2min", "int", "25"]
        variables = [mylist1, mylist2]  # TODO: self.__controller.get_variables()
        for data in variables:
            row = []
            for item in data:
                i = QStandardItem(str(item))
                row.append(i)
            self.__model.appendRow(row)

    def set_selected_config(self, index: int):
        self.__controller.select_config(self.combo_process_type.currentIndex())

    def set_config_settings_item(self, item: QTreeWidgetItem):
        raise NotImplementedError  # TODO: IMPLEMENTIEREN

    def _handle_data_changed(self, top_left: QStandardItem, bottom_right: QStandardItem):
        """When a field is changed by the user this function is called to find the row that has been changed.

        Args:
            top_left (QStandardItem): _description_
            bottom_right (QStandardItem): _description_
        """
        for row in range(top_left.row(), bottom_right.row() + 1):
            for column in range(top_left.column(), bottom_right.column() + 1):
                self.__current_row = row

    def _handle_selection_change(self):
        """Gets the currently selected row and gives it to the widget to know."""
        self._selected_rows = self.__table.selectionModel().selectedRows()
