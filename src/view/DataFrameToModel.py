from PyQt5.QtCore import QAbstractTableModel, Qt


class DataFrameToModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def rowCount(self, parent=None):
        return self.data.shape[0]  # returns number of rows

    def columnCount(self, parent=None):
        return self.data.shape[1]  # returns the number of columns

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return str(self.data.iloc[row, column])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.data.columns[section])
            else:
                return str(self.data.index[section])
