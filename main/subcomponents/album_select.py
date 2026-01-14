from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Signal)
from PySide6.QtGui import (QPixmap)

from PySide6.QtWidgets import (QApplication, QLabel, QScrollArea, QHBoxLayout, QSizePolicy, QVBoxLayout,
    QWidget, QPushButton, QListView, QDialog)

from .album_grid_view_components import Album, AlbumSongListModel, SongItemDelegate, SongMetadataEditor
from .album_select_widgets import SongView
from ..song import Song

class AlbumSelect(QWidget):
    returning_song = Signal(Song, str)


    def __init__(self, album : Album, parent = None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.album = album

        self.cover_title_box = QWidget(self)
        self.cover_title_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.cover_title_box.setMinimumSize(QSize(600, 250))
        self.cover_title_box_layout = QHBoxLayout(self.cover_title_box)
        self.cover_Label = QLabel(self.cover_title_box)
        self.cover_Label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.cover_Label.setMinimumSize(QSize(200, 200))
        self.title_Label = QLabel(self.cover_title_box)
        self.title_Label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.title_Label.setMinimumSize(QSize(0, 200))

        self.cover_title_box_layout.addWidget(self.cover_Label)
        self.cover_title_box_layout.addWidget(self.title_Label,alignment=Qt.AlignBottom)

        self.layout.addWidget(self.cover_title_box)

        self.song_view = QListView()
        self.album_model = AlbumSongListModel(album)
        self.delegate = SongItemDelegate(self.song_view)
        self.song_view.setItemDelegate(self.delegate)
        self.delegate.song_pressed.connect(self.return_song)
        self.delegate.to_modify_song.connect(self.modify_song)

        self.song_view.setModel(self.album_model)
        self.song_view.setIconSize(QSize(40,40))  # must set icon size

        # # --- Scrollable album area ---
        # self.scrollArea = QScrollArea()
        # self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # # --- Content inside scroll area ---
        # self.song_list = QWidget()
        # self.song_list_layout = QVBoxLayout(self.song_list)
        # self.song_list_layout.setContentsMargins(10, 10, 10, 10)
        # self.song_list_layout.setSpacing(20)
        # self.scrollArea.setWidget(self.song_list)

        self.layout.addWidget(self.song_view)
        self.update_ui()

        # --- Back button ---
        self.back_button = QPushButton("← Back")
        self.back_button.setFixedHeight(40)
        self.layout.addWidget(self.back_button)

    def _reload_preview(self, art_bytes):
        if art_bytes:
            pixmap = QPixmap()
            pixmap.loadFromData(art_bytes)

            pixmap = pixmap.scaled(
                self.cover_Label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        else:
            pixmap = QPixmap(200, 200)
            pixmap.fill(Qt.gray)

        self.cover_Label.setPixmap(pixmap)
    
    def _clear(self):
        while self.song_list_layout.count():
            item = self.song_list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def update_ui(self):
        songs = self.album.get_songs()
        info = self.album.info_check()
        self.title_Label.setText(f"{info[0]} \n{info[1]}")
        length = len(songs)
        self._reload_preview(self.album.get_cover())

    def return_song(self,idx, mode):
        song = self.album.get_song(idx)
        self.returning_song.emit(song, mode)
        print(f"album select emitted on mode {mode}")
    
    def modify_song(self, idx):
        song = self.album.get_song(idx)
        dialog = SongMetadataEditor(song, self)
        if dialog.exec() == QDialog.Accepted:
            song.update(**dialog.get_metadata())
            if dialog.art_bytes:
                song.set_art_bytes(dialog.art_bytes)
