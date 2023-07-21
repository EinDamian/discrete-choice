from __future__ import annotations
import os

from PyQt5.QtCore import QSortFilterProxyModel, Qt, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QComboBox, QLineEdit, QTreeView, QAbstractItemView
from PyQt5 import uic

from src.config import ConfigFunctionHighlighting, ConfigProcessingWidget
from src.controller.calculation.ConfigurationController import ConfigurationController
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.view.FunctionHighlightDelegate import FunctionHighlightDelegate


class ProcessingWidget(QWidget):
    """Display for the free variables and the Choice variable"""

    # Signal for communication with the other widgets in the main window to update
    processing_update_signal = pyqtSignal()

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
        """Gets the current information from the model and displays it."""

        """def _apply_error_report(function: FunctionalExpression, label: str) -> QStandardItem:
            Adds the highlights of the mistakes found in the definition of functions to the item displayed in the table.
            The error messages are put into a ToolTip and the string markers are applied as highlights.

            Args:
                label (str): Label
                function (FunctionalExpression): Functional expression to be put into the item.

            Returns:
                QStandardItem: The item containing the functional expression with its mistakes highlighted.

            item = QStandardItem(function.expression)
            error_report = self.__controller.get_error_report(label)

            if error_report.valid:
                return item

            # set the highlighting of the errors on the item in the table
            error_text = ConfigFunctionHighlighting.MISTAKE_TOOLTIP_START
            highlights = []  # highlight format is [(start, end, "#FF00AA")]
            for single_marker in error_report.marker:
                highlights.append(
                    (single_marker.begin, single_marker.end, single_marker.color_hex))
                error_text += ConfigFunctionHighlighting.LIST_CHARACTER_MISTAKES_TOOLTIP + \
                              function.expression[single_marker.begin: single_marker.end + 1] + \
                              ": " + single_marker.message  # TODO: besser
            item.setData(highlights, Qt.UserRole + 1)
            item.setToolTip(error_text)

            return item"""

        # combo box update
        config_names = self.__controller.get_config_display_names()
        config_idx = self.__controller.get_project().get_selected_config_index()
        self.combo_box.clear()
        if config_names is not None:
            for name in config_names:
                self.combo_box.addItem(name)
        self.combo_box.setCurrentIndex(config_idx)

        # clear the model for the tree view to add updated data
        self.__model.clear()
        self.__model.setHorizontalHeaderLabels(ConfigProcessingWidget.HEADERS)

        # get the data from the model and add it to the table
        variables = self.__controller.get_project().get_derivative_free_variables()
        values_dict = self.__controller.get_project().get_config_settings()[self.combo_box.currentIndex()]
        value = FunctionalExpression("")
        choice = self.__controller.get_project().get_choice()
        if choice is not None:
            c_row = []
            c = QStandardItem(ConfigProcessingWidget.CHOICE)
            c.setEditable(False)
            c_row.append(c)
            c_value = QStandardItem(choice.expression)
            c_row.append(c_value)
            self.__model.appendRow(c_row)
        for data in variables:
            key = data
            if key in values_dict:
                value = values_dict[key]
            row = []
            i = QStandardItem(data)
            i.setEditable(False)
            row.append(i)
            v = QStandardItem(value.expression)  # _apply_error_report(value, data)
            row.append(v)
            self.__model.appendRow(row)

        super().update()

    def initiate_update(self):
        """Function used to send the signal to the Main window so that everything gets updated."""
        self.processing_update_signal.emit()

    def set_selected_config(self):
        """Sets the selected config using the current index."""
        pass#self.__controller.select_config(self.combo_box.currentIndex())

    def set_config_settings_item(self, name: str, value: str):
        """
        Adds or changes the variable to the config_settings .
        :param name: the variable's name
        :param value: the variable's value
        :return:
        """
        self.__controller.update_settings_item(name, value)

    def _data_changed(self, top_left: QStandardItem, bottom_right: QStandardItem):
        """When a field is changed by the user this function is called to find the row that has been changed.

        Args:
            top_left (QStandardItem): _description_
            bottom_right (QStandardItem): _description_
        """
        for row in range(top_left.row(), bottom_right.row() + 1):
            for column in range(top_left.column(), bottom_right.column() + 1):
                self.__current_row = row
        name = self.__model.item(self.__current_row).text()
        value = self.__model.item(self.__current_row, 1).text()
        self.set_config_settings_item(name, value)
