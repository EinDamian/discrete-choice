from __future__ import annotations

from PyQt5.QtWidgets import QMenuBar, QMenu


class Menu(QMenu):
    """
    This class represents an abstarct menu. Only specific menus include more functions,
    as they provide the user with different operations.
    """
    def __init__(self, parent: QMenuBar):
        """
        Initializes a menu. All menus must have a parent
        @param parent: The Menu bar, where the menu belongs
        @type parent: QMenuBar
        """
        super().__init__(parent)
