from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QColor


class DataFrameToModel(QAbstractTableModel):
    def __init__(self, data, thresholds: dict):
        super().__init__()
        self.data = data
        self.thresholds = thresholds

    def rowCount(self, parent=None):
        return self.data.shape[0]  # returns number of rows

    def columnCount(self, parent=None):
        return self.data.shape[1]  # returns the number of columns

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            cell_value = self.data.iloc[row, column]
            threshold = list(self.thresholds.values())[column]

            if cell_value > threshold:
                return {
                    'value': str(cell_value),
                    'background_color': QColor(211, 211, 211)
                }
            else:
                return {
                    'value': str(cell_value),
                    'background_color': None
                }
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.data.columns[section])
            else:
                return str(self.data.index[section])
