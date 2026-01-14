from PySide6.QtCore import (QSize, QTime, QUrl, Qt, Signal)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QGridLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar, QScrollArea,
    QVBoxLayout, QWidget)

from .album_grid_view_components import Album, AlbumWidget, AlbumIndexer
from ..song import Song


COLUMNS = 2

class AlbumGridView(QWidget):
    album_clicked = Signal(object)  # emits Album instance

    def __init__(self, parent = None):
        super().__init__(parent)
        self.album_indexer = AlbumIndexer()
        self.album_indexer.album_changed.connect(self.update_ui)

        # --- Scrollable album area ---
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(QSize(520, 640))


        # --- Content inside scroll area ---
        self.widget = QWidget()
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(10)
        self.scrollArea.setWidget(self.widget)

        layout = QVBoxLayout(self)
        layout.addWidget(self.scrollArea)


    def _clear(self):
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def set_songs(self, songs: list[Song]):
        self.album_indexer.set_songs(songs)
        self.update_ui(self.album_indexer.get_albums())

    def update_ui(self, albums: list[Album]):
        self._clear()
        for album in albums:
            self.add_album(album)

    def add_album(self, album: Album):
        index = self.gridLayout.count()
        row = index // COLUMNS  # COLUMNS = 4
        col = index % COLUMNS

        album_widget = AlbumWidget(album, self.widget)
        self.gridLayout.addWidget(album_widget, row, col, alignment=Qt.AlignTop | Qt.AlignLeft)
        album_widget.clicked.connect(lambda checked=False, a=album: self.album_clicked.emit(a))