from PySide6.QtCore import (QObject, QPoint, QRect,QSize, QTime, QUrl, Qt, Signal)
from PySide6.QtGui import QPixmap, QIcon, QPainter, QColor

from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy, QScrollArea,
    QSlider, QSpacerItem, QStackedWidget, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

ICONS = {
    "previous" : ":/assets/icons/ChevronLeft.svg", 
    "pause" : ":/assets/icons/Pause.svg",
    "next" : ":/assets/icons/ChevronRight.svg"
}

def colored_icon(path, color):
    pixmap = QPixmap(path)
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color))
    painter.end()
    return QIcon(pixmap)


class PreviousPauseNext(QWidget):
    perform_action = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName(u"widget_6")
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))
        self.layout = QHBoxLayout(self)
        self.buttons : dict = {}
        self.layout.addStretch()
        
        for name, icon in ICONS.items():
            btn = QPushButton(self)
            btn.setIcon(colored_icon(icon, "white"))
            btn.setIconSize(QSize(60, 60))
            print(name)
            btn.clicked.connect(lambda checked=False, n=name: self.perform_action.emit(n))
            self.layout.addWidget(btn)
            self.buttons[name] = btn

        # print(self.buttons)
        self.layout.addStretch()

