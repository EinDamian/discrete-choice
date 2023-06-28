from __future__ import annotations

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    from view.MainWindow import MainWindow

    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
