from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap, QIcon, QPainter, QColor
from PySide6.QtWidgets import (QButtonGroup, QApplication, QPushButton, QHBoxLayout, QGridLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QToolButton, QSizePolicy, QStatusBar, QScrollArea,
    QVBoxLayout, QWidget)

from .album_grid_view_components import AlbumWidget, AlbumProvider
from ..song import Song

ICONS = {
    "player" : ":/assets/icons/Player.svg", 
    "song search" : ":/assets/icons/Search.svg",
    "playlist" : ":/assets/icons/Playlists.svg", 
    "album" : ":/assets/icons/Albums.svg",
    "downloader" : ":/assets/icons/Downloader.svg",
    "settings" :  ":/assets/icons/Settings.svg",
    "visualiser" : ":/assets/icons/Visualiser.svg",

}

def colored_icon(path, color):
    pixmap = QPixmap(path)
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color))
    painter.end()
    return QIcon(pixmap)


class NavigationBar(QWidget):
    toggle_queue = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.logo = QLabel(self)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        pixmap = QPixmap(":/assets/icons/ringo_music.jpg").scaled(
            60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.logo.setPixmap(pixmap)
        self.logo.setFixedSize(60, 60)
        self.logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo, alignment=Qt.AlignCenter)

        for idx, (name, icon) in enumerate(ICONS.items()):
            btn = QToolButton(self)
            btn.setIcon(QIcon(icon))
            btn.setIconSize(QSize(40, 40))
            btn.setCheckable(True)
            btn.setAutoRaise(True)

            self.button_group.addButton(btn, idx)
            self.layout.addWidget(btn, alignment=Qt.AlignCenter)

        self.queue_button = QPushButton(self)
        self.queue_button.setText("Queue")
        self.queue_button.pressed.connect(self.toggle_queue)
        self.layout.addWidget(self.queue_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()
