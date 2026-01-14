from PySide6.QtCore import (Qt)
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QButtonGroup, QApplication, QPushButton, QHBoxLayout, QGridLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QToolButton, QSizePolicy, QStatusBar, QScrollArea,
    QVBoxLayout, QWidget)

from .album_grid_view_components import Album, AlbumWidget, AlbumIndexer
from ..song import Song


class NavigationBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.logo = QLabel(self)
        self.logo.setText("🎵")
        self.logo.setStyleSheet("font-size: 32px;")
        self.layout.addWidget(self.logo, alignment = Qt.AlignCenter)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        self.album_button = QToolButton(self)
        self.player_button = QToolButton(self)
        self.visualiser_button = QToolButton(self)

        for btn, text, idx in (
            (self.album_button, "Albums", 0),
            (self.player_button, "Player", 1),
            (self.visualiser_button, "Visualiser", 2),
        ):
            btn.setText(text)
            btn.setCheckable(True)
            btn.setAutoRaise(True)

            self.button_group.addButton(btn, idx)
            self.layout.addWidget(btn, alignment = Qt.AlignCenter)
        self.layout.addStretch(1)


        # Default selection
        self.album_button.setChecked(True)
    