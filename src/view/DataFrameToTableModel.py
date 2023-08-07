from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QColor


class DataFrameToTableModel(QAbstractTableModel):
    """
    This class is used to create a table model from a DataFrame(Evaluation), so
    it can be inserted into QTableView in EvaluationWidget GUI.
    """
    def __init__(self, data, thresholds: dict):
        """
        Initializes a new table model
        @param data: The Evaluation
        @type data: DataFrame
        @param thresholds: the thresholds to be applied on the evaluation
        @type thresholds: dictionary, where the columns (string) are the keys
            and the thresholds (float) are the thresholds
        """
        super().__init__()
        self.data = data
        self.thresholds = thresholds

    def rowCount(self, parent=None):
        """
        This returns the number of rows in the data
        @param parent: the parent is not relevant here,  because there is no need for hierarchical model
        @type parent: None
        @return: numer of rows
        @rtype: int
        """
        return self.data.shape[0]

    def columnCount(self, parent=None):
        """
        This returns the number of columns in the data
        @param parent: not relevant here,  because there is no need for hierarchical model
        @type parent: None
        @return: number of columns
        @rtype: int
        """
        return self.data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        """
        Assigns the data to the model. It also considers the thresholds.
        If a call contains a value higher than the given threshold, it will be colored
        @param index: index of the data item, where the actual (requested) data is found
        @type index: QModelIndex
        @param role: Qt.DisplayRole stands for the item's element's role.
                    An element with this role contains the key data to be rendered in from of a text
        @type role: int
        @return: The value to be displayed and the cell's color
        @rtype:
        """
        row = index.row()
        column = index.column()
        cell_value = self.data.iloc[row, column]
        threshold = list(self.thresholds.values())[column]

        if cell_value > threshold:
            return {
                    'value': str(cell_value),
                    'background_color': QColor(128, 128, 128, alpha=128)
            }
        else:
            return {
                'value': str(cell_value),
                'background_color': None
            }

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        This functions enables to set custom labels for the columns and indexes in the table.
        @param section: the index of the header item
        @type section: int
        @param orientation: specifies whether the item is for columns or indexes
        @type orientation: Orientation
        @param role: stands for the item's element's role.
                    An element with this DisplayRole contains the key data to be rendered in from of a text
        @type role: Qt.DisplayRole int
        @return: the text to be displayed
        @rtype: str
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.data.columns[section])
            else:
                return str(self.data.index[section])