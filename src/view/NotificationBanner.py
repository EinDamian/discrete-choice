from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from src.config import ConfigNotificationBanner as Cfg


class NotificationBanner(QWidget):
    """
    This class represents a notification banner. This is used in the MainWindow to inform the user,
    where to find the user manual after the program starts.
    """
    def __init__(self, text, timeout=Cfg.timeout):
        super().__init__()
        self.text = text
        self.timeout = timeout

        layout = QVBoxLayout()
        self.label = QLabel(self.text)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setStyleSheet("background-color: rgba%s;" % Cfg.rgba_color)  # Semi-transparent white background
        self.setFixedHeight(Cfg.banner_height)  # Set the desired height for the banner

        self.timer = QTimer()
        self.timer.timeout.connect(self.close)
        self.timer.start(self.timeout)

        self.show()
