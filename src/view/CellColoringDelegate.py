from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QFont
from PyQt5.QtWidgets import QStyledItemDelegate


class CellColoringDelegate(QStyledItemDelegate):
    """
    This custom delegate is used for coloring the cells in the evaluation table, which
    contain values higher than the given thresholds.
    It also makes these values appear in bold font
    """
    def paint(self, painter, option, index):
        """
        Renders the delegate using the given painter and style option for the item
        specified by index
        @param painter: the painter
        @type painter: QPainter
        @param option: the style option
        @type option: QStyleOptionViewItem
        @param index: the index of the item
        @type index: QModelIndex
        """
        painter.save()
        data = index.data(Qt.DisplayRole)
        value = data['value']
        bg_color = data['background_color']

        if bg_color is not None:
            painter.fillRect(option.rect, QBrush(bg_color))
            font = QFont(option.font)
            font.setBold(True)
            painter.setFont(font)
        painter.drawText(option.rect, Qt.AlignCenter, str(value))
        painter.restore()
