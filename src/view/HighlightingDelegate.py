from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtWidgets import QStyledItemDelegate


class HighlightingDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        data = index.data(Qt.DisplayRole)
        value = data['value']
        bg_color = data['background_color']

        if bg_color is not None:
            painter.fillRect(option.rect, QBrush(bg_color))
            font = QFont(option.font)
            font.setBold(True)
            painter.setFont(font)
        painter.drawText(option.rect, Qt.AlignCenter, str(value))
