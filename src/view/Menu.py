from __future__ import annotations

from PyQt5.QtWidgets import QMenuBar, QMenu


class Menu(QMenu):
    def __init__(self, parent: QMenuBar):
        super().__init__(parent)
