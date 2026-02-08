from PySide6.QtCore import (QSize, QTime, QUrl, Qt, Signal)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QGridLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar, QScrollArea,
    QVBoxLayout, QWidget)

from .playlist_grid_view_components import PlaylistWidget, PlaylistProvider
from ..library_manager import LibraryService, PlaylistMeta


COLUMNS = 2

class PlaylistGridView(QWidget):
    playlist_clicked = Signal(object)  # emits Playlist instance

    def __init__(self, library : LibraryService, parent = None):
        super().__init__(parent)
        self.playlist_provider = PlaylistProvider(library)
        self.playlist_provider.playlists_changed.connect(self.update_ui)
        self.lib = library

        # --- Scrollable playlist area ---
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
        self.update_ui(self.playlist_provider.get_playlists())

    def _clear(self):
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()


    def update_ui(self, playlists: list[PlaylistMeta]):
        self._clear()
        for playlist in playlists:
            self.add_playlist(playlist)

    def add_playlist(self, playlist: PlaylistMeta):
        index = self.gridLayout.count()
        row = index // COLUMNS  # COLUMNS = 4
        col = index % COLUMNS

        playlist_widget = PlaylistWidget(playlist, self.widget)
        self.gridLayout.addWidget(playlist_widget, row, col, alignment=Qt.AlignTop | Qt.AlignLeft)
        playlist_widget.clicked.connect(lambda checked=False, p=playlist: self.playlist_clicked.emit(p))