from __future__ import annotations
import os

from PyQt5.QtWidgets import (
    QToolButton,
    QWidget,
    QTreeView,
    QDialog,
    QFileDialog,
    QAbstractItemView,
    QLineEdit
)
from PyQt5.QtCore import QModelIndex, QSortFilterProxyModel, Qt, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import uic

from src.controller.functions.AlternativeController import AlternativeController
from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.view.FileManagementWindow import FileManagementWindow
from src.view.UserInputDialog import UserInputDialog
from src.view.FunctionHighlightDelegate import FunctionHighlightDelegate
from src.view.UIUtil import display_exceptions
from src.config import ConfigErrorMessages, ConfigModelWidget, ConfigFunctionHighlighting


class ModelWidget(QWidget):
    """Display of the existing alternatives."""
    
    # Signal for communication with the other widgets in the main window to update
    model_update_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # load ui file created with Qt Creator
        uic.loadUi(f'{os.path.dirname(__file__)}/ui/model.ui', self)

        self.__controller: AlternativeController = AlternativeController()

        addButton = self.findChild(QToolButton, "add_button")
        addButton.clicked.connect(self.add)
        exportButton = self.findChild(QToolButton, "export_button")
        exportButton.clicked.connect(self.export)
        importButton = self.findChild(QToolButton, "import_button")
        importButton.clicked.connect(self.import_)
        removeButton = self.findChild(QToolButton, "remove_button")
        removeButton.clicked.connect(self.remove)

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
        self.__table.selectionModel().selectionChanged.connect(
            self._handle_selection_change)

        self.__delegate = FunctionHighlightDelegate(parent=self.__table)
        self.__table.setItemDelegate(self.__delegate)
        self.__model.dataChanged.connect(self._handle_data_changed)

        self.update()

    def update(self):
        """Gets the current information from the model and displays it.
        """
        super().update()

        def _apply_error_report(label: str, function: FunctionalExpression, availability: bool = False) -> QStandardItem:
            """Adds the highlights of the mistakes found in the definition of functions to the item displayed in the table.
            The error messages are put into a ToolTip and the string markers are applied as highlights.

            Args:
                label (str): Label of the Alternative
                function (FunctionalExpression): Functional expression to be put into the item.

            Returns:
                QStandardItem: The item containing the functional expression with its mistakes highlighted.
            """
            item = QStandardItem(function.expression)

            if availability:
                error_report = self.__controller.get_availability_condition_error_report(
                    label)
            else:
                error_report = self.__controller.get_error_report(label)

            if error_report.valid:
                return item

            # set the highlighting of the errors on the item in the table
            error_text = ConfigFunctionHighlighting.MISTAKE_TOOLTIP_START
            # format is [(1, 3, "#FF00F0"), (4, 9, "#0000F0")]
            highlights = []

            for single_marker in error_report.marker:
                highlights.append(
                    (single_marker.begin, single_marker.end, single_marker.color_hex))
                error_text += ConfigFunctionHighlighting.LIST_CHARACTER_MISTAKES_TOOLTIP + \
                    single_marker.message
            item.setData(highlights, Qt.UserRole + 1)
            item.setToolTip(error_text)

            return item

        # get the data from the model and make a list out of it
        alternative_dict = self.__controller.get_alternatives()

        # label need to be saved to know them after they have been changed
        self.__labels = []

        # clear the model for the tree view to add updated data
        self.__model.clear()
        headers = ConfigModelWidget.HEADERS
        self.__model.setHorizontalHeaderLabels(headers)

        # iterate through all the alternatives to be displayed.
        for label, alternative in alternative_dict.items():
            row = [QStandardItem(label), _apply_error_report(label,
                                                             alternative.function), _apply_error_report(label, alternative.availability_condition, availability=True)]
            self.__labels.append(label)
            self.__model.appendRow(row)
            
    def initiate_update(self):
        """Function used to send the signal to the Main window so that everything gets updated.
        """
        self.model_update_signal.emit()

    @display_exceptions
    def add(self):
        """Adds a new alternative. Opens an input window for user input."""
        dialog = UserInputDialog(
            ConfigModelWidget.HEADERS, ConfigModelWidget.BUTTON_NAME_ADDITION, ConfigModelWidget.WINDOW_TITLE_ADDITION)
        if dialog.exec_() == QDialog.Accepted:
            label, functional_expression, availability = dialog.get_user_input()
        else:
            return
        self._add_alternative(label, availability, functional_expression)

    @display_exceptions
    def remove(self):
        """Removes the alternative of currently selected row."""
        labels = self._get_selected_labels()
        if labels is not None and len(labels) > 0:
            for label in labels:
                self.__controller.remove(label.text())
                self.initiate_update()
        else:
            raise AttributeError(
                ConfigErrorMessages.ERROR_MSG_NO_ALTERNATIVE_SELECTED)

    @display_exceptions
    def change(self):
        """Detects the made changes and applies them in the model. Happens for each modified field."""
        row_index = self.__current_row
        index_label = self.__model.index(
            row_index, ConfigModelWidget.INDEX_LABEL, QModelIndex())
        index_definition = self.__model.index(
            row_index, ConfigModelWidget.INDEX_DEFINITION, QModelIndex())
        index_availability = self.__model.index(
            row_index, ConfigModelWidget.INDEX_AVAILABILITY, QModelIndex())
        old_label = self.__labels[row_index]
        new_label = self.__model.itemFromIndex(index_label).text()
        new_definition = self.__model.itemFromIndex(index_definition).text()
        new_availability = self.__model.itemFromIndex(
            index_availability).text()

        # if the label stayed the same the function was changed, else the old label needs to be removed
        if new_label == old_label:
            self.__controller.change(
                label=new_label, availability=new_availability, function=new_definition)
            self.initiate_update()
        else:
            self.__controller.change(
                label=new_label, availability=new_availability, function=new_definition)
            self.__controller.remove(label=old_label)
            self.initiate_update()

    @display_exceptions
    def export(self):
        """Exporting the selected alternative as a json file.
        """
        if self._get_selected_labels() is not None and len(self._get_selected_labels()) > 0:
            labels = [l.text() for l in self._get_selected_labels()]
            path = self._select_path()
            self.__controller.export(path, labels)
        else:
            raise AttributeError(
                ConfigErrorMessages.ERROR_MSG_NO_ALTERNATIVE_SELECTED)

    @display_exceptions
    def import_(self):
        """Importing JSON files containing a new alternative.
        """
        paths = self._select_files()
        if paths is not None:
            for path in paths:
                self.__controller.import_(path)
        self.initiate_update()

    @display_exceptions
    def _add_alternative(self, label: str, availability: str, definition: str):
        """Adding of an Alternative to the model via the controller.

        Args:
            label (str): The label of the new alternative.
            definition (str): The definition of the new alternative.
        """
        self.__controller.add(label, availability, definition)
        self.initiate_update()

    def _handle_selection_change(self, current, previous):
        """Gets the currently selected row and gives it to the widget to know.

        Args:
            current (QModelIndex): The index of the selected row in the model.
        """
        self._selected_rows = self.__table.selectionModel().selectedRows()

    def _handle_data_changed(self, topLeft: QStandardItem, bottomRight: QStandardItem):
        """When a field is changed by the user this function is called to find the row that has been changed.

        Args:
            topLeft (QStandardItem): _description_
            bottomRight (QStandardItem): _description_
        """
        self.__current_row = topLeft.row()
        self.change()

    def _get_selected_labels(self):
        """Gets the currently selected label from the view."""
        try:
            labels = []
            for row in self.__table.selectionModel().selectedRows():
                index_label = self.__model.index(
                    row.row(), ConfigModelWidget.INDEX_LABEL, QModelIndex())
                label = self.__model.itemFromIndex(index_label)
                labels.append(label)
            return labels
        except AttributeError as exception:
            raise AttributeError(
                ConfigErrorMessages.ERROR_MSG_NO_ALTERNATIVE_SELECTED) from exception

    def _select_path(self) -> str:
        """Opens a file dialog for the user to choose a directory. Only one can be chosen.

        Returns:
            str:The path to the chosen directory.
        """
        return FileManagementWindow().open_file(ConfigModelWidget.ALTERNATIVE_EXPORT_WINDOW_TITLE, QFileDialog.Directory, "")

    def _select_files(self) -> list[str]:
        """Helper function to select files for import.

        Returns:
            list[str]: List of paths of the selected files by the user.
        """
        return FileManagementWindow().choose_files(ConfigModelWidget.ALTERNATIVE_IMPORT_WINDOW_TITLE, QFileDialog.ExistingFiles, ConfigModelWidget.FILE_TYPE_FILTER_ALTERNATIVE_IMPORT)
