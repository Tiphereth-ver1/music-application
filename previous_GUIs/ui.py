from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

from .swappable import Swappable
from .subcomponents import QueueHistoryDisplay

class Ui_MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.leftbar = QWidget(self)
        self.leftbar.setMinimumSize(QSize(150, 0))
        self.leftbar.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Expanding)
        self.swappable = Swappable(self)
        self.swappable.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.swappable.setMinimumSize(QSize(450, 0))
        self.rightbar = QueueHistoryDisplay(self)
        self.rightbar.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.rightbar.setMinimumSize(QSize(250, 0))

        self.layout.addWidget(self.leftbar)
        self.layout.addWidget(self.swappable)
        self.layout.addWidget(self.rightbar)


