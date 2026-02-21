from PySide6.QtCore import (QSize, QTime, QUrl, Qt, Signal)
from PySide6.QtWidgets import (QGridLayout, QSizePolicy, QLabel, QScrollArea, QVBoxLayout, QWidget, QComboBox)

from .album_grid_view_components import AlbumWidget, AlbumProvider
from ..library_manager import LibraryService, AlbumMeta, RETURN_VALUES


COLUMNS = 3

SORT_TYPES = {"ID" : RETURN_VALUES.ID, 
                "Title" : RETURN_VALUES.TITLE, 
                "Artist" : RETURN_VALUES.ALBUM_ARTIST,
                "Year" : RETURN_VALUES.YEAR}

class AlbumGridView(QWidget):
    album_clicked = Signal(object)  # emits Album instance
    send_sort_type = Signal(RETURN_VALUES)

    def __init__(self, library : LibraryService, parent = None):
        super().__init__(parent)
        self.album_provider = AlbumProvider(library)
        self.album_provider.albums_changed.connect(self.update_ui)
        self.lib = library

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

        self.layout = QVBoxLayout(self)

        self.sortComboBox = QComboBox(self)
        self.sortComboBox.addItems(SORT_TYPES.keys())
        self.sortComboBox.setMinimumWidth(50)

        self.sortComboBox.currentIndexChanged.connect(self.select_sort_type)
        self.send_sort_type.connect(self.album_provider.update_sort_type)

        self.layout.addWidget(self.sortComboBox)
        self.layout.addWidget(self.scrollArea)

        self.update_ui(self.album_provider.get_albums())

    def _clear(self):
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def select_sort_type(self):
        print(SORT_TYPES[self.sortComboBox.currentText()])
        self.send_sort_type.emit(SORT_TYPES[self.sortComboBox.currentText()])

    def update_ui(self, albums: list[AlbumMeta]):
        self._clear()
        for album in albums:
            self.add_album(album)

    def add_album(self, album: AlbumMeta):
        index = self.gridLayout.count()
        row = index // COLUMNS  # COLUMNS = 4
        col = index % COLUMNS

        album_widget = AlbumWidget(album, self.lib.art_cache, self.widget)
        self.gridLayout.addWidget(album_widget, row, col, alignment=Qt.AlignTop | Qt.AlignLeft)
        album_widget.clicked.connect(lambda checked=False, a=album: self.album_clicked.emit(a))