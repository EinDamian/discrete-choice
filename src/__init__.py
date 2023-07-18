from __future__ import annotations

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from src.view.MainWindow import MainWindow

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
