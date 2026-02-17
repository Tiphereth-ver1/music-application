from PySide6.QtCore import (QSize, Signal)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget)
from PySide6.QtGui import QPixmap, QIcon, QPainter, QColor

def colored_icon(path, color):
    pixmap = QPixmap(path)
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color))
    painter.end()
    return QIcon(pixmap)

ICONS = {
    "shuffle" : ":/assets/icons/Plus.svg", 
    "loop" : ":/assets/icons/Repeat.svg"
}


class ShuffleLoop(QWidget):
    perform_action = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))
        self.setMinimumSize(QSize(500, 60))
        self.internal_layout = QHBoxLayout(self)
        self.buttons : dict = {}

        self.internal_layout.addStretch()
        for name, icon in ICONS.items():
            btn = QPushButton(self)
            btn.setIcon(colored_icon(icon, "white"))
            btn.setIconSize(QSize(60, 60))
            btn.clicked.connect(lambda checked=False, n=name: self.perform_action.emit(n))
            self.internal_layout.addWidget(btn)
            self.buttons[name] = btn

        self.internal_layout.addStretch()
