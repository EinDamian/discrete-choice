from PyQt5.QtCore import Qt, QModelIndex, QRect
from PyQt5.QtGui import QColor, QPainter, QFontMetrics
from PyQt5.QtWidgets import QStyledItemDelegate

from src.config import ConfigFunctionHighlighting


class FunctionHighlightDelegate(QStyledItemDelegate):
    """Highlighter for the Functions that contain errors"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.alpha = ConfigFunctionHighlighting.OPACITY

    def paint(self, painter: QPainter, option: 'QStyleOptionViewItem', index: QModelIndex):
        """Highlighting the Functions that contain errors

        Args:
            painter (QPainter): The painter needed for coloring.
            option (QStyleOptionViewItem): Option of highlighting.
            index (QModelIndex): The index of the Item in the table to be colored. Contains the highlighting data.
        """
        painter.save()
        super().paint(painter, option, index)

        rect = option.rect
        text = index.data(Qt.DisplayRole)
        # highlights have format [(start, end, color)]
        highlights = index.data(Qt.UserRole + 1)
        if highlights == None:
            painter.restore()
            return

        # iterating through all needed highlights
        for start, end, color in highlights:
            highlight_rect = self.calculateHighlightRect(
                rect, text, start, end)
            adjusted_color = self.adjustColorOpacity(QColor(color))
            painter.fillRect(highlight_rect, adjusted_color)

        painter.restore()

    def calculateHighlightRect(self, rect: QRect, text: str, start: int, end: int) -> QRect:
        """The text cannot be marked individually, so the width of the highlights need to be calculated.

        Args:
            rect (QRect): Text rectangle of the cell.
            text (str): The text in the cell.
            start (int): The starting index from where the text should be colored.
            end (int): The ending index to which the text should be colored.

        Returns:
            QRect: Rectangle to be highlighted.
        """

        #
        text_rect = QRect(rect)
        fm = QFontMetrics(self.parent().font())
        text_width = fm.boundingRect(text).width()
        text_rect.setWidth(text_width)

        start_x = text_rect.left() + fm.horizontalAdvance(text[:start]) + ConfigFunctionHighlighting.HIGHLIGHTING_OFFSET
        end_x = text_rect.left() + fm.horizontalAdvance(text[:end]) + ConfigFunctionHighlighting.HIGHLIGHTING_OFFSET
        highlight_rect = QRect(start_x, text_rect.top(),
                               end_x - start_x, text_rect.height())
        return highlight_rect

    def adjustColorOpacity(self, color: int) -> QColor:
        """Apply the color and opacity.

        Args:
            color (int): The hexadecimal rgb value of the wanted color.

        Returns:
            QColor: The final color of the highlight.
        """
        adjusted_color = QColor(color)
        adjusted_color.setAlpha(self.alpha)
        return adjusted_color
