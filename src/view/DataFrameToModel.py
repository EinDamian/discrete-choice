from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QColor


class DataFrameToModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.set_highlighted_cells = set()

    def rowCount(self, parent=None):
        return self.data.shape[0]  # returns number of rows

    def columnCount(self, parent=None):
        return self.data.shape[1]  # returns the number of columns

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return str(self.data.iloc[row, column])
        elif role == Qt.BackgroundRole:
            if index in self.set_highlighted_cells:
                return QColor(220, 220, 220)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.data.columns[section])
            else:
                return str(self.data.index[section])

    def set_highlighted_cells(self, cells):
        self.set_highlighted_cells = cells
        self.data.emit(
            self.index(0, 0),
            self.index(self.rowCount() - 1,
                       self.columnCount() - 1))