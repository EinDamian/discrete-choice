from __future__ import annotations
import os
import re

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

from src.model.data.functions.FunctionalExpression import FunctionalExpression
from src.view.FileManagementWindow import FileManagementWindow
from src.view.UserInputDialog import UserInputDialog
from src.view.FunctionHighlightDelegate import FunctionHighlightDelegate
from src.view.UIUtil import display_exceptions
from src.config import ConfigErrorMessages, ConfigColumnWidget, ConfigRegexPatterns, ConfigFunctionHighlighting
from src.controller.functions.DerivativeController import DerivativeController


class ColumnWidget(QWidget):
    """The Widget represents the table with the derivatives and imported data in its columns."""

    # Signal for communication with the other widgets in the main window to update
    column_update_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(f'{os.path.dirname(__file__)}/ui/columns.ui',
                   self)  # load ui file created with Qt Creator

        self.__controller: DerivativeController = DerivativeController()

        # connect buttons to widget and the according functions
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

        self.__highlighting_delegate = FunctionHighlightDelegate(
            parent=self.__table)
        self.__table.setItemDelegate(self.__highlighting_delegate)
        self.__number_variables = 0
        self.__model.dataChanged.connect(self.change)

        self.update()

    def update(self):
        """Function that gets the current Data from the model via the controller and puts the derivatives and data in the table"""

        def _apply_error_report(function: FunctionalExpression, label: str) -> QStandardItem:
            """Adds the highlights of the mistakes found in the definition of functions to the item displayed in the table.
            The error messages are put into a ToolTip and the string markers are applied as highlights.

            Args:
                label (str): Label
                function (FunctionalExpression): Functional expression to be put into the item.

            Returns:
                QStandardItem: The item containing the functional expression with its mistakes highlighted.
            """
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
                    function.expression[single_marker.begin: single_marker.end +
                                        1] + ": " + single_marker.message  # TODO: besser
            item.setData(highlights, Qt.UserRole + 1)
            item.setToolTip(error_text)

            return item

        # clear the model for the tree view to add updated data
        self.__labels = []
        self.__model.clear()
        self.__model.setHorizontalHeaderLabels(ConfigColumnWidget.HEADERS)

        def datatype_to_string(datatype: type) -> str:
            """Transforms a datatype to the string that will be displayed.
            Either the <class> brackets will be removed or the numbers of the pandas datatypes will be removed.

            Args:
                datatype (type): The Datatype to be displayed.

            Returns:
                str: The String that will be put in the table.
            """
            if datatype is None:
                return ConfigColumnWidget.FILLER_UNDETERMINED_DATATYPE

            d_type_splitted = str(datatype).split(
                "'")  # Python format is e.g. <class 'bool'>
            if len(d_type_splitted) > 2 and re.fullmatch(ConfigRegexPatterns.PATTERN_DATATYPES, d_type_splitted[-2]):
                return d_type_splitted[-2]
            else:
                # pandas datatypes shown as regular datatypes without bit number
                d_type = str(datatype).split(".")[-1]# numpy datatypes may have format numpy.<datatype><number>
                search = re.search(
                    ConfigRegexPatterns.PATTERN_DATATYPES, d_type)
                return d_type[search.start(): search.end()]

        def make_uneditable_item(content: str) -> QStandardItem:
            """Makes the grayed out standard items for the uneditable variables shown.

            Args:
                content (str): The content in the cell.

            Returns:
                QStandardItem: The item to be placed in the table.
            """
            item = QStandardItem(content)
            item.setEditable(False)
            item.setEnabled(False)
            return item

        # get the data from the model and add it uneditable to the table
        raw_data_variables = self.__controller.get_variables()
        self.__number_variables = len(raw_data_variables)

        # set the variables once into the table but uneditable and unselectable
        for variable in raw_data_variables:
            self.__model.appendRow([make_uneditable_item(variable), make_uneditable_item(datatype_to_string(
                raw_data_variables[variable])), make_uneditable_item(ConfigColumnWidget.FILLER_EMPTY_DEFINITION)])

        # display derivatives
        derivative_dict = self.__controller.get_derivatives()

        # iterate through all the derivative to be displayed.
        for label, derivative in derivative_dict.items():
            row = [QStandardItem(label), make_uneditable_item(
                datatype_to_string(self.__controller.get_derivative_type(label))), _apply_error_report(derivative, label)]
            self.__labels.append(label)
            self.__model.appendRow(row)

        super().update()

    def initiate_update(self):
        """Function used to send the signal to the Main window so that everything gets updated
        """
        self.column_update_signal.emit()

    @display_exceptions
    def add(self):
        """Adds a new derivative. Opens an input window for user input."""
        dialog = UserInputDialog(
            [ConfigColumnWidget.HEADERS[ConfigColumnWidget.INDEX_LABEL], ConfigColumnWidget.HEADERS[ConfigColumnWidget.INDEX_DEFINITION]], ConfigColumnWidget.BUTTON_NAME_ADDITION, ConfigColumnWidget.WINDOW_TITLE_ADDITION)
        if dialog.exec_() == QDialog.Accepted:
            label, functional_expression = dialog.get_user_input()
        else:
            return  # when x pressed
        self.__controller.add(label, functional_expression)
        self.initiate_update()

    @display_exceptions
    def remove(self):
        """Removes the derivative of currently selected row. If no derivatives are selected an error is shown."""
        labels = self._get_selected_labels()
        if labels is not None and len(labels) > 0:
            for label in labels:
                self.__controller.remove(label.text())
            self.initiate_update()
        else:
            raise AttributeError(
                ConfigErrorMessages.ERROR_MSG_NO_DERIVATIVE_SELECTED)

    @display_exceptions
    def change(self, topLeft: QModelIndex, bottomRight: QModelIndex, changed_roles: list[int]):
        """Function that applies changes made in the table to the model. Only one cell can be changed at a time.

        Args:
            topLeft (QModelIndex): Index of the label of the changed row.
            bottomRight (QModelIndex): Index of the definition of the changed row.
            changed_roles (list[int]): The changed roles of the changed item.
        """
        row_index = topLeft.row(
        )  # row where the change happened. The other arguments point to the same row
        index_label = self.__model.index(
            row_index, ConfigColumnWidget.INDEX_LABEL, QModelIndex())
        index_definition = self.__model.index(
            row_index, ConfigColumnWidget.INDEX_DEFINITION, QModelIndex())
        old_label = self.__labels[row_index - self.__number_variables]
        new_label = self.__model.itemFromIndex(index_label).text()
        new_definition = self.__model.itemFromIndex(index_definition).text()

        # if the label stayed the same the function was changed, else the old label needs to be removed
        if new_label == old_label:
            self.__controller.change(
                label=new_label, function=new_definition)
            self.initiate_update()
        else:
            self.__controller.change(
                label=new_label, function=new_definition)
            self.__controller.remove(label=old_label)
            self.initiate_update()

    @display_exceptions
    def export(self):
        """Exporting the selected derivative as a json file."""
        if self._get_selected_labels() is not None and len(self._get_selected_labels()) > 0:
            labels = [l.text() for l in self._get_selected_labels()]
            path = self._select_path()
            self.__controller.export(path, labels)
        else:
            raise AttributeError(
                ConfigErrorMessages.ERROR_MSG_NO_DERIVATIVE_SELECTED)

    @display_exceptions
    def import_(self):
        """Importing JSON files containing new derivatives.
        """
        paths = self._select_files()
        if paths is not None:
            for path in paths:
                self.__controller.import_(path)
        self.initiate_update()

    def _get_selected_labels(self):
        """Gets the currently selected label from the view."""
        try:
            labels = []
            for row in self.__table.selectionModel().selectedRows():
                index_label = self.__model.index(
                    row.row(), ConfigColumnWidget.INDEX_LABEL, QModelIndex())
                label = self.__model.itemFromIndex(index_label)
                labels.append(label)
            return labels
        except AttributeError as exception:
            raise AttributeError(
                ConfigErrorMessages.ERROR_MSG_NO_DERIVATIVE_SELECTED) from exception

    def _select_path(self) -> str:
        """Opens a file dialog for the user to choose a directory. Only one can be chosen.

        Returns:
            str:The path to the chosen directory.
        """
        return FileManagementWindow().open_file(ConfigColumnWidget.DERIVATIVE_EXPORT_WINDOW_TITLE, QFileDialog.Directory, "")

    def _select_files(self) -> list[str]:
        """Opens a file dialog to select a json file.

        Returns:
            list[str]: The paths of the selected files.
        """
        return FileManagementWindow().choose_files(ConfigColumnWidget.DERIVATIVE_IMPORT_WINDOW_TITLE, QFileDialog.ExistingFiles, ConfigColumnWidget.FILE_TYPE_FILTER_DERIVATIVE_IMPORT)
