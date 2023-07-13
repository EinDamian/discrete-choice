from PyQt5.QtCore import Qt, QModelIndex, QRect
from PyQt5.QtGui import QColor, QPainter, QFontMetrics
from PyQt5.QtWidgets import QStyledItemDelegate


class HighlightDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.highlights = []
        self.alpha = 128  # Default opacity value

    def paint(self, painter: QPainter, option: 'QStyleOptionViewItem', index: QModelIndex):
        painter.save()
        super().paint(painter, option, index)

        rect = option.rect
        text = index.data(Qt.DisplayRole)
        highlights = index.data(Qt.UserRole + 1)
        if highlights == None:
            painter.restore()
            return
        # highlights = [(1, 3, "#FF00F0"), (4, 6, "#0000F0")]

        for start, end, color in highlights:
                highlight_rect = self.calculateHighlightRect(rect, text, start + 1, end)
                adjusted_color = self.adjustColorOpacity(QColor(color))
                painter.fillRect(highlight_rect, adjusted_color)

        painter.restore()

    def calculateHighlightRect(self, rect, text, start, end):
        text_rect = QRect(rect)
        fm = QFontMetrics(self.parent().font())
        text_width = fm.boundingRect(text).width()
        text_rect.setWidth(text_width)

        start_x = text_rect.left() + fm.horizontalAdvance(text[:start])
        end_x = text_rect.left() + fm.horizontalAdvance(text[:end])
        highlight_rect = QRect(start_x, text_rect.top(), end_x - start_x, text_rect.height())
        return highlight_rect

    def adjustColorOpacity(self, color):
        adjusted_color = QColor(color)
        adjusted_color.setAlpha(self.alpha)
        return adjusted_color